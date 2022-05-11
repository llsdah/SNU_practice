pragma solidity >0.7.0 <0.8.0;


/*
토큰이랑 ?특정 블록체인 플랫폼에서 동작하는 응용 서비스에서만 사용하는 암호화폐.
1. r 이라는 사람이 회원관리 할것이다.  주소 1234
2. 처음 deployg하면 토큰은 이다. 

동작 과정 
owered 맴버쉽관리의 주인입니다. 
w 



*/


contract Owned {
    address public owner;
    event OwnershipTransfer(address _oldAddr, address _newAddr);
    // 계약자 주인이 바꿨을 때 발생하는 이벤트?
    modifier onlyOwner() { require(msg.sender == owner, "Only owner can run this function"); _; }
    // Designate contract distributor as contract owner
    // 주인이야 아니냐 확인 주인만 계약자 변경이 가능합니다. 

    constructor() {
    // 배포한 사람의 주소를 입력합니다.  
    
        owner = msg.sender;
    }

    // Transfer contract ownership
    function transferOwnership(address _newAddr) public onlyOwner {
    // 계약자의 주인을 바꾸는 함수입니다. 
        address oldAddr = owner; 
        owner = _newAddr;
        emit OwnershipTransfer(oldAddr, owner);// 이벤트 발생시키 겠다 . 
    }

}// owned

contract Membership is Owned { 
    // 회원관리 장부 입니다 'is' 상속을 받는다는 의미 여기에서는 Owned를 상속 받는다는 의미입니다.
    // 향후 NFT의 보안을 위해 사용하기도 합니다. 

    struct MembershipLevel {
    // 구조체 : 여러가지 변수를 넣기 위해 정의 합니다.  
        string name; // Membership name
        uint256 times; // Minimum number of transactions required to achieve the grade
        uint256 sum; // Minimum transaction amount required to achieve the grade
        int8 rate; // Cashback Rate
    }//membershiplevel

    struct History {
    // 거래 이력 저장, 위한 구조체 
        uint256 times; // Cumulative number of transactions
        uint256 sum; // Cumulative transaction amount
        uint256 levelIndex; // Current membership grade index
        // 왜 했다 효율적으로 짜기 위해, 그 기준을 또 불러오기 귀찮아 한번에 해결
    }// History
    
    address public tokenAddr; // 토큰의 주소가 들어간 공간. 
    MembershipLevel [] public levels; // 구조체 배열, 
    mapping(address => History) public tradingHistory; //사용자에 따른 거래이력 가지고 오는 것 
    // input == address, output == history

    modifier onlyToken() { require(msg.sender == tokenAddr, "This function is not for users"); _; }
    // 제가 지정한 토큰 계약에서만 한다. tokenaddr 저장 일치가 필요합니다. 
    
    // constructor omitted (inheritance)
    // Interworking between smart contracts
    function setToken(address _tokenAddr) public onlyOwner {
    // 토큰 관리용 
        tokenAddr = _tokenAddr;
    }


    function pushLevel(string memory _name, uint256 _times, uint256 _sum, int8 _rate) public onlyOwner {
    // 등급 정보 입력합니다.  
        levels.push(MembershipLevel({
                name : _name,
                times : _times,
                sum : _sum,
                rate : _rate} 
                                ) 
        );
    
    }//pushlevel
    
    function editLevel(uint256 _index, string memory _newName, uint256 _newTimes,
                            uint256 _newSum, int8 _newRate) public onlyOwner {
        require(_index < levels.length); 
        //길이보다 작아야 됩니다.!!! 당연한 것입니다. 

        levels[_index].name = _newName;
        levels[_index].times = _newTimes;
        levels[_index].sum = _newSum;
        levels[_index].rate = _newRate;
    }// editlevel

    function updateHistory(address _member, uint256 _value) public onlyToken {
    // 거래 이력 변경은.. 해당 토큰만 가능하다.. 토큰과. 

        tradingHistory[_member].times += 1; // 거래 이력변경이니까 거래 수 증가 
        tradingHistory[_member].sum += _value; // 거래 금액도 변경해야됨.
        uint256 index = tradingHistory[_member].levelIndex;// 해야 위치를 저장해야됨
        int8 tmpRate; // 향후 임시저장위한 변수 생성. 
    
        for (uint i = 0; i < levels.length; i++) {
            // 모든 회원등급 탐색합니다. 
            if (tradingHistory[_member].times >= levels[i].times
                && tradingHistory[_member].sum >= levels[i].sum
                && tmpRate < levels[i].rate) {
                    index = i;
                    tmpRate = levels[i].rate;
                    // 계속 반복되니까 결국 남는것 최고의 rate가 됩니다. 
            }
        }
        tradingHistory[_member].levelIndex = index;// 회원관리 명부에 들어가 있는 index 
    }//updateHistory
    
    function getCashbackRate(address _member) public view returns (int8 rate) {
    // 가지고 올 rate
        rate = levels[tradingHistory[_member].levelIndex].rate;
    }
}

contract MyTokenWithFeatures is Owned{

    uint256 public totalSupply; // uint256 == uint 총급량정보 
    mapping (address => uint256) public balanceOf; // 밸런스 여부 
    mapping (address => mapping(address => uint256)) private approved;// 권한 위임 여부
    mapping (address => Membership) public memberships; // 맴버쉽 변수  추가된 부분 입니다. 

    string public name;
    string public symbol;
    uint256 public decimals;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

    // Blacklist
    mapping (address => uint8) public blacklist;
    event Blacklisted(address indexed _address);
    event DeletedFromBlacklist(address indexed _address);
    event RejectedPaymentToBlacklistedAddr(address indexed _from, address indexed _to, uint256 _value);
    event RejectedPaymentFromBlacklistedAddr(address indexed _from, address indexed _to, uint256 _value);
    event Cashback(address indexed _from, address indexed _to, uint256 _cashback);


    constructor (string memory _name, string memory _symbol, 
                 uint256 _supply, uint256 _decimals) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        
        balanceOf[msg.sender] = _supply * 10 ** _decimals;
        totalSupply = _supply * 10 ** _decimals;
    }

    function setMembership(Membership _membershipAddr) public {
    //자신의 장부에만 영향이 갈 수 있도록 합니다. 자신의 장부만 운영할 수 있도록??!
    // A라는 사람이 멤버쉽 장부를 토큰에 등록합니다. 
        memberships[msg.sender] = Membership(_membershipAddr);
    }// 

    
    function isBlacklisted(address _address) public view returns (bool inBlacklist) {
        inBlacklist = blacklist[_address] == 1;
		return inBlacklist;
    }

    function pushBlacklist(address _address) public onlyOwner {
        // 다양한 해커 분들도 막을 수 있음. 
        blacklist[_address] = 1;
        emit Blacklisted(_address);
    }


    function deleteFromBlacklist(address _address) public onlyOwner {
        blacklist[_address] = 0;
        emit DeletedFromBlacklist(_address);
    }

    function isValidTransfer(address _from, address _to, uint256 _value) 
    internal view returns (bool isValid) {
        if (balanceOf[_from] >= _value && balanceOf[_to] + _value >= balanceOf[_to]) {
            isValid = true;
        } else {
            isValid = false;
        }

        return isValid;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        // 돈 전송 부분 입니다.
        if (isBlacklisted(msg.sender)) {
            emit RejectedPaymentFromBlacklistedAddr(msg.sender, _to, _value);
            success = false;
        } else if (isBlacklisted(_to)) {
            emit RejectedPaymentToBlacklistedAddr(msg.sender, _to, _value);
            success = false;
        } else if (isValidTransfer(msg.sender, _to, _value)) {
            // 일단  코드 수정도 필요합니다. 이부분 
            uint256 cashBackRate = uint256(memberships[_to].getCashbackRate(msg.sender));
            // 토큰 받는 사람 = _to가 회원장부 등록이 안되어 있으면 에러 발생될것입
            // 즉, 돈 받는사람이 관리하는 장부에 접근해 해당 돈 받는사람이 보내는 사람에 대해 cashbankrate 불러옴
            uint256 cashback = _value * cashBackRate / 100;
            memberships[_to].updateHistory(msg.sender, _value);
            //거래 금액도 증가 , 회원관리 장부 업데이트 합니다. 

            _value -= cashback;
            emit Cashback(msg.sender, _to, cashback);
            
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            
            emit Transfer(msg.sender, _to, _value);
            success = true;
        } else {
            success = false;
        }

        return success;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        // 권한 위임부분입니다. 
        if (approved[msg.sender][_spender] + _value >= approved[msg.sender][_spender]) {
            approved[msg.sender][_spender] = approved[msg.sender][_spender] + _value;

            emit Approval(msg.sender, _spender, _value);
            success = true;
        } else {
            success = false;
        }
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        remaining = approved[_owner][_spender];
        return remaining;
    }
	
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (isBlacklisted(_from)) {
            emit RejectedPaymentFromBlacklistedAddr(_from, _to, _value);
            success = false;
        } else if (isBlacklisted(_to)) {
            emit RejectedPaymentToBlacklistedAddr(_from, _to, _value);
            success = false;
        } else if (allowance(_from, msg.sender) > 0 && allowance(_from, msg.sender) >= _value && isValidTransfer(_from, _to, _value)) {
            // 권한 주었는지 확인. 금액도 확인 필요 입니다. 
            uint256 cashBackRate = uint256(memberships[_to].getCashbackRate(_from));
            uint256 cashback = _value * cashBackRate / 100;
            memberships[_to].updateHistory(_from, _value);

            _value -= cashback;
            emit Cashback(msg.sender, _to, cashback);
            
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            approved[_from][msg.sender] -= _value;// 위임받은 금액도 차감 . 

            emit Transfer(_from, _to, _value);
            success = true;
        } else {
            success = false;
        }

        return success;
    }
}



