pragma solidity >= 0.7.0 < 0.8.0;

/* 8장토큰

ICO : 

IEO : 제한된 투자자 받는다. 거래소의 회원들만 참여가능 자격제한. (바이낸스)
    거래소 상장 직전에 자격조건 갗추고 거래소를 통한 판매, 신뢰성증가

STO : security token 사업에 대한 주식을 주는 것처럼? 예시) 부동산 토큰
    해당 사업과 연계좌 토큰 발행, 전통적인 자산기반 가상화폐 발행, 주주처럼


*/

// [1] 소유권 관리 계약

contract Owned {
    address public owner;
    event OwnershipTransfer(address _oldAddr, address _newAddr);
    modifier onlyOwner() { require(msg.sender == owner); _; }
    
    constructor() {
        owner = msg.sender;
    }
    
    function transferOwnership(address _newAddr) public onlyOwner {
        address oldAddr = owner;
        owner = _newAddr;
        emit OwnershipTransfer(oldAddr, owner);
    }
}

// [2] 토큰 계약
contract MyToken is Owned{
    uint256 public totalSupply; // uint256 == uint
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping(address => uint256)) private approved;

    string public name;
    string public symbol;
    uint256 public decimals;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

    constructor (string memory _name, string memory _symbol, 
                 uint256 _supply, uint256 _decimals) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        
        balanceOf[msg.sender] = _supply * 10 ** _decimals;
        totalSupply = _supply * 10 ** _decimals;
    }

    function isValidTransfer(address _from, address _to, uint256 _value) internal view returns (bool isValid) {
        if (balanceOf[_from] >= _value && balanceOf[_to] + _value >= balanceOf[_to]) {
            isValid = true;
        } else {
            isValid = false;
        }

        return isValid;
    }
    
    function transfer(address _to, uint256 _value) public returns (bool success) {
        if (isValidTransfer(msg.sender, _to, _value)) {
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
        if (allowance(_from, msg.sender) > 0 && isValidTransfer(_from, _to, _value)) {
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

// [3] 토큰 크라우드 세일 이부분이 추가된 것입니다. 
contract Crowdsale is Owned {
    uint256 public fundingGoal;
    uint256 public startTime; // 시작
    uint256 public deadline; // 마지막
    uint256 public price; // 가격
    uint256 public transferableToken;
    uint256 public soldToken;
    MyToken public tokenReward;
    bool public fundingGoalReached; // 참여 가능여부 
    bool public isOpened; // 열려 있는지. 
    mapping (address => Property) public fundersProperty; // 자금 
    
    // 구조체: 자금 제공자 정보
    struct Property {
        uint256 paymentEther;
        uint256 reservedToken;
        bool withdrawed;
    }
    
    // 이벤트 선언
    event CrowdsaleStart(uint fundingGoal, uint deadline, uint transferableToken, address beneficiary);
    event ReservedToken(address backer, uint amount, uint token);
    event CheckGoalReached(address beneficiary, uint fundingGoal, uint amountRaised, bool reached, uint raisedToken);
    event WithdrawalToken(address addr, uint amount, bool result);
    event WithdrawalEther(address addr, uint amount, bool result);
    
    // 판매 종료 이후에만 실행되게끔 지정하는 수식자
    modifier afterDeadline() { 
        require(block.timestamp >= deadline); 
        _; 
    }
    
    // 생성자
    constructor(uint _fundingGoalInEthers, uint _transferableToken, uint _amountOfTokenPerEther, MyToken _tokenAddr) {
        // 발행 후 진행 해야됨왜? 토큰 주소 넣어야되니까 . 
        fundingGoal = _fundingGoalInEthers * 1 ether; 
        price = 1 ether / _amountOfTokenPerEther; // 1 이더당 얼마 주나요
        transferableToken = _transferableToken; // 전환될 토큰인가융?
        tokenReward = MyToken(_tokenAddr); // 토큰 계약의 주소 
    }
    
    // 추가 토큰 지급 비율
    function currentSwapRate() public view returns(uint) {
        if (startTime + 3 minutes > block.timestamp) { 
            return 100; 
        } else if (startTime + 5 minutes > block.timestamp) { 
            return 50; 
        } else if (startTime + 10 minutes > block.timestamp) { 
            return 20; 
        } else { 
            return 0; 
        }
    }// currentSwapRate
    
    // 펀딩 금액 예치 함수
    function reserve() public payable {  
    // 이더리움 송금 부분?
        require(isOpened && block.timestamp < deadline);
        // 클라우드 세일오픈 여부 
        
        uint amount = msg.value;
        uint token = amount * (100 + currentSwapRate()) / price / 100;
        // 지금  보너스 됀 
        
        require(token > 0 && soldToken + token <= transferableToken);
        
        fundersProperty[msg.sender].paymentEther += amount; // 참가 내역에 접근 해서 증가하고. 
        fundersProperty[msg.sender].reservedToken += token;
        soldToken += token;
        emit ReservedToken(msg.sender, amount, token);
    }// reserve()
    
    // 크라우드 세일 개시
    function start(uint _durationInMinutes) public onlyOwner {
        require(fundingGoal > 0 && price > 0);
        require(address(tokenReward) > address(0) && transferableToken > 0 
            && tokenReward.balanceOf(address(this)) >= transferableToken);
        // contract 주소 == address(this),  
        require(_durationInMinutes > 0 && startTime == 0);
        
        startTime = block.timestamp;
        deadline = block.timestamp + _durationInMinutes * 1 minutes;
        isOpened = true;

        emit CrowdsaleStart(fundingGoal, deadline, transferableToken, owner);
    }
    
    // 잔여 시간, 목표 금액, 토큰 확인
    function getRemainingTimeEthToken() public view returns(uint min, int shortage, uint remainToken) {
        if (block.timestamp < deadline) {
            min = (deadline - block.timestamp) / (1 minutes);
        }
		shortage = int256(fundingGoal - address(this).balance) / (1 ether); 
		remainToken = transferableToken - soldToken;// 부족분. (음수면 다 충족함) 
    }
	
	// 목표 달성 여부 확인
	function checkGoalReached() public afterDeadline {
		require(isOpened);
		
		if (address(this).balance >= fundingGoal) {
			fundingGoalReached = true;
		}
		
		isOpened = false;
		emit CheckGoalReached(owner, fundingGoal, address(this).balance, fundingGoalReached, soldToken);
	}
	
	// 토큰 발행자용 인출 함수
	function withdrawalOwner() public onlyOwner {

		require(!isOpened);
        // 진행중에 출금 하면안댐 
		
		if (fundingGoalReached) {
		    uint amount = address(this).balance;
            // 출금할 금액이 있습니다. 
		    if (amount > 0) {
		        bool result = payable(msg.sender).send(amount);
                // owner payable(msg.sender) ==  돈을 받을 수 있는 주소로 변환하고. 전송해줌. 
		        emit WithdrawalEther(msg.sender, amount, result);
		    }
		    
		    uint val = transferableToken - soldToken;
            // 남은양?? 팔리고 남은양  발행 - 판거 

		    if (val > 0) {
                // 남은거 
		        tokenReward.transfer(msg.sender, transferableToken - soldToken);
                // 남은양을 토큰 배포자에게 돌려줍니다. 
		        emit WithdrawalToken(msg.sender, val, true);
		    }
		} else {
            // 없으면 
		    uint val = tokenReward.balanceOf(address(this));
		    tokenReward.transfer(msg.sender, val);
		    emit WithdrawalToken(msg.sender, val, true);
		}
	}
	
	// 크라우드 세일 참여자용 인출 함수
	function withdrawal() public {
	    require(!isOpened);
	    require(!fundersProperty[msg.sender].withdrawed);
        // 돈을 뺸사람은 코드 실행 필요가 없습니다. 
		if (fundingGoalReached) {
            if (fundersProperty[msg.sender].reservedToken > 0) {
                tokenReward.transfer(msg.sender, fundersProperty[msg.sender].reservedToken);
                // 받은 코튼 만큼 돈 보내 주기 
                fundersProperty[msg.sender].withdrawed = true;
                // 정산완료
                emit WithdrawalToken(msg.sender, fundersProperty[msg.sender].reservedToken, fundersProperty[msg.sender].withdrawed);
            }
		} else {
            // 정산적으로 실행이 안될떄, 즉, 모금액 보다 적게 모였을때, 참여자 들은 토큰이 아니라 이더를 받아야합니다. 
            if (fundersProperty[msg.sender].paymentEther > 0) {

                if (payable(msg.sender).send(fundersProperty[msg.sender].paymentEther)) {
                    // 이더를 받아야와서 줍니다. 
                    fundersProperty[msg.sender].withdrawed = true;
                    // 정산 끝 
                }
                emit WithdrawalEther(msg.sender, fundersProperty[msg.sender].reservedToken, fundersProperty[msg.sender].withdrawed);
            }
		}
	}// withdrawal
}