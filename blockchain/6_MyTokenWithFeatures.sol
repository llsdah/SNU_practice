pragma solidity >0.7.0 <0.8.0;

// 기 MyToken과 유사 
contract MyTokenWithFeatures{
    uint256 public totalSupply; // uint256 == uint
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping(address => uint256)) private approved;

    string public name;
    string public symbol;
    uint256 public decimals;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

    // For the blacklist and membership
    address public manager; // 관리자 즉, 기업 

    modifier onlyManager() {
        // manager만 관리자만 가능확인용
        require(msg.sender == manager, "Only the manager can call this function.");
        _;
    }

    // Blacklist
    mapping (address => uint8) public blacklist;
    // 0 1 로 표시 

    event Blacklisted(address indexed _address);
    event DeletedFromBlacklist(address indexed _address);
    event RejectedPaymentToBlacklistedAddr(address indexed _from, address indexed _to, uint256 _value);
    event RejectedPaymentFromBlacklistedAddr(address indexed _from, address indexed _to, uint256 _value);
    // 거래 기록용 입니다. 이것을 향후 UIUX에서 구현하거나 거래 기록용을 나타냅니다. 

    // Membership
    mapping (address => uint8) public memberships;
    uint256 public cashbackRate;    // 0-100, 100 means 100%
    // 캐시백 비율 설정 

    event Cashback(address indexed _from, address indexed _to, uint256 _cashback);
    // 배당주듯이 인센티브? 개념??

    constructor (string memory _name, string memory _symbol, 
                 uint256 _supply, uint256 _decimals) {
        manager = msg.sender;
        
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        
        balanceOf[msg.sender] = _supply * 10 ** _decimals;
        totalSupply = _supply * 10 ** _decimals;
    }//contract



    function isBlacklisted(address _address) public view returns (bool inBlacklist) {
        // 블랙 리스트 등재 확인용 
        inBlacklist = blacklist[_address] == 1;// 등재 되면 1이다.
		return inBlacklist;
    }//isblack

    function pushBlacklist(address _address) public onlyManager {
    // 블랙리스크 관리자 우선 확인 ,  블랙리스트입력 
        blacklist[_address] = 1;
        emit Blacklisted(_address);
    }

    function deleteFromBlacklist(address _address) public onlyManager {
    // 삭제
        blacklist[_address] = 0;
        emit DeletedFromBlacklist(_address);
    }// black del

    function setMembership(address _address, uint8 _isMember) public onlyManager {
    // 회원이면 1? 아니면 0으로 구현 예정 
        memberships[_address] = _isMember;
    }

    function setCashbackRate(uint256 _cashbackRate) public onlyManager {
    // 캐시백 얼마 할지 설정용 
        require(_cashbackRate >= 0 && _cashbackRate <= 100, "Invalid cashback rate.");
        cashbackRate = _cashbackRate;
    }//set cachback

    function isValidTransfer(address _from, address _to, uint256 _value) 
    internal view returns (bool isValid) {
        if (balanceOf[_from] >= _value && balanceOf[_to] + _value >= balanceOf[_to]) {
            isValid = true;
        } else {
            isValid = false;
        }

        return isValid;
    }// isvaildtransfer

    function transfer(address _to, uint256 _value) public returns (bool success) {
    // 거래 실행용 코드
        
        if (isBlacklisted(msg.sender)) { // 블랙리스트 등재 확인용
            emit RejectedPaymentFromBlacklistedAddr(msg.sender, _to, _value);
            success = false;
        } else if (isBlacklisted(_to)) {
            emit RejectedPaymentToBlacklistedAddr(msg.sender, _to, _value);
            success = false;
        } else if (isValidTransfer(msg.sender, _to, _value)) { // 거래 가능 확인용
            if (_to == manager) { // 결제 하자마자 할인.
            // 맴버쉽일 경우만 할일 해주면됩니다. && memberships[msg.sender]==1
                uint256 cashback = _value * cashbackRate / 100;
                _value -= cashback;
                emit Cashback(msg.sender, _to, cashback);// 바로 보내 주기 
            }

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
        // 위임해서 송금하니까 실행하는 사람과 보내는 사람이 다릅니다. 
        if (isBlacklisted(_from)) {
            emit RejectedPaymentFromBlacklistedAddr(_from, _to, _value);
            success = false;
        } else if (isBlacklisted(_to)) {
            emit RejectedPaymentToBlacklistedAddr(_from, _to, _value);
            success = false;
        } else if (allowance(_from, msg.sender) > 0 && isValidTransfer(_from, _to, _value)) {
            // if( allowance(_from, msg.sender) >= _value) 해당 내용 추가 필요합니다. 
            
            if (_to == manager) {
                uint256 cashback = _value * cashbackRate / 100;
                _value -= cashback;
                emit Cashback(msg.sender, _to, cashback);
            }

            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            approved[_from][msg.sender] -= _value;

            emit Transfer(_from, _to, _value);
            success = true;
        } else {
            success = false;
        }

        return success;
    }
}