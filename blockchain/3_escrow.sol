// SPDX-License-Identifier: GPL-3.0

/**
4/20 
큰 코드의 순서 Escrow-> buy-> sell
**/
pragma solidity >=0.7.0 <0.8.0;
contract Escrow {
	address public buyer; // address of buyer's wallet
	address public seller; // address of seller's wallet
	address private escrow; // address of intermediary's wallet (private)
	uint private start; // timestamp of contract creation

	bool buyerOk; 
	bool sellerOk; 

    bool temp; // 계약 완료 후 재 입금 불가 하도록 하는것 

    modifier onlyBuyer {
        require(msg.sender == buyer, "Only buyer can call this function");
        _;} 

    //  buy 와 sell는 scrow가 되면 안된다. 
	constructor(address buyer_address, address seller_address) {
        
        require( (buyer_address != msg.sender) &&(seller_address != msg.sender), "Escrow dont have buyer or seller");

		buyer = buyer_address; 
		seller = seller_address; 
		escrow = msg.sender; 
		start = block.timestamp; 
	}

	function deposit() public payable onlyBuyer{
		require(temp ==false);
	}

    // 한번 성사된 거래는 다시 돈을 못 넣게 한다. 
	function payBalance() private { // 돈주고 받는 함수 입니다. 
        require(msg.value > 0.001*1 ether

        );
		//payable(escrow).transfer(address(this).balance / 100); // pay a fee for escrow 정률 거래 
		if(address(this).balance <0.01 * 1 ether){
            payable(escrow).transfer(address(this).balance / 100);
        }else{
            payable(escrow).transfer(0.001*1 ether); // pay a fee for escrow
        }
        
    
        payable(seller).transfer(address(this).balance);
	}
// self destruct 문제 
    //양방 승인으로 거래가 발생하느것
	function accept() public {
	
		if (msg.sender == buyer){
			buyerOk = true;
		} else if (msg.sender == seller){
			sellerOk = true;
		}

		if (buyerOk && sellerOk){
			payBalance(); //모두 승인하면 대금 지급
            temp = true;
		} else if (buyerOk && !sellerOk && block.timestamp > start + 30 days) {
			selfdestruct(payable(buyer)); // destruct automatically when more than 30 days elapsed with only the buyer's approval
            temp = true;
		}
	}
    
    // 취소 누른 상환
	function cancel() public {
		if (msg.sender == buyer){
			buyerOk = false;
		} else if (msg.sender == seller){
			sellerOk = false;
		} 

		if (!buyerOk && !sellerOk){
			selfdestruct(payable(buyer)); // destruct when the contract is not approved by calling the cancel function
		}
	}
    // 수상한 거래도 escrow가 거래 중단. 
	function kill() public  {
		if (msg.sender == escrow) {
			selfdestruct(payable(buyer)); // destruct if the escrow kill this contract
            temp = true;
        }
        
	}

    // 거래 상황 확인용 
	function view_balance() public view returns (uint){return address(this).balance;}


}