pragma solidity >0.7.0 <0.8.0;

contract MyToken{
    uint256 public totalSupply; // uint256 == uint, 부호없는 숫자형 public 파란색 버튼 
    mapping (address => uint256) public balanceOf;// 주소입력시 uint256 값 반환 주소의 잔고 저장합니다. 
    mapping (address => mapping(address => uint256)) private approved;
    //nest mapping 이중 맵핑 맴핑된것을 다시 맵핑해서 키를 여러개 받을 수 있도록 합니다. 단, 키가 어떤 내용인지 분명히 알기!  
    // add -> add -> uint, 키1이 키2에 승인해준 금액 
    
    string public name; // 토큰의 이름
    string public symbol; // symbol 거래소에서 나타낼 약어
    uint256 public decimals;// decimals 소수점연산이 안되기에 연산 단위 나타내는 것 

    
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    // 송금이 일어 났다면. 반드시 기록되어야됨,! 0원 송금도 반드시 송금 기록 
    // indexed 특별한 예약어 ? index 넣어주는 아이 정도 간단하게 기억 

    event Approval(address indexed _owner, address indexed _spender, uint256 _value); 
    // 성공되었다면 알려주는 것이다. 


    constructor (string memory _name, string memory _symbol,    
                 uint256 _supply, uint256 _decimals) {  
    // 토큰 이름, 토큰 약어, 단위 지정입니다.  supply == 발행할 토큰의 수 
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        
        balanceOf[msg.sender] = _supply * 10 ** _decimals; // 갯수 곱하기 금액 ! 총 잔액
        totalSupply = _supply * 10 ** _decimals;
    }

    function isValidTransfer(address _from, address _to, uint256 _value) internal view returns (bool isValid) {
        // 송금이 실제 유효한지
        // tranfer 수행 되든 안되든 아무것도 안되면 ->  default 
        // send 실제 실행되면서 되었다 안되었다 bool 반환
        
        if (balanceOf[_from] >= _value && balanceOf[_to] + _value >= balanceOf[_to]) {
        // 보내는 사람 잔고 확인, 받는 사람의 잔고가 표현할 수 있는 범위를 넘어가는 경우를 방지하기 위해 
            isValid = true;
        } else {
            isValid = false;
        }

        return isValid;
    }
    
    function transfer(address _to, uint256 _value) public returns (bool success) {
        // 송금하는 함수

        if (isValidTransfer(msg.sender, _to, _value)) {
            // 정상적인 송금이라면
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;

            emit Transfer(msg.sender, _to, _value);// 기록용입니다. 
            success = true;
        } else {
            success = false;
        }

        return success;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        // 위임장 주는 함수 누구한테 위임 spender, 얼마만큼 위임
        
        if (approved[msg.sender][_spender] + _value >= approved[msg.sender][_spender]) {
        // 위임받은 금액이 새로추가된 위임금액이 값이 적어지지 않도록????

            approved[msg.sender][_spender] = approved[msg.sender][_spender] + _value;

            emit Approval(msg.sender, _spender, _value);
            // 네트워크상 기록을 위해 한다. 노드?같은 개념인가유?

            success = true;
        } else {
            success = false;
        }
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        // 값을 받아오는것이  ower가 spender에게 위임해준 금액을 반환?

        remaining = approved[_owner][_spender];
        return remaining;
    }
	
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        // 다른사람도 실행 가능,, 누가 누구에게서 토큰이 갔는지. from ===owner

        if (allowance(_from, msg.sender) > 0 && isValidTransfer(_from, _to, _value)) {
            // 추가로 allowance(_from, msg.sender) >= _value 추가해야됨
            // 위임 받았는지 여부를 체크 합니다. 승인받은 잔액이 있는지, 그리고 유효한 송금인지, 
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            approved[_from][msg.sender] -= _value; // if문 추가해야됨. 승인받은 금액이 있는지 . 

            emit Transfer(_from, _to, _value); // 기록용.
            success = true;
        } else {
            success = false;
        }

        return success;
    }
}