/* How to run:
code = fs.readFileSync('Media.sol').toString()
solc = require('solc')
compiledCode = solc.compile(code)
abiDefinition = JSON.parse(compiledCode.contracts[':Media'].interface)
VotingContract = web3.eth.contract(abiDefinition)
byteCode = compiledCode.contracts[':Media'].bytecode
deployedContract = VotingContract.new((web3.eth.accounts), {data: byteCode, from: web3.eth.accounts[0], gas: 4700000})
contractInstance = VotingContract.at(deployedContract.address)
contractInstance.validateCreator(web3.eth.accounts[0], {from: web3.eth.accounts[0]})
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[0])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[1])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[2])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[3])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[4])).toString()

var key = new NodeRSA(['f43b06b070f9312ea5a0e8046056194e0f6f381f71c11ce1982c1c5e8e434b52', []]);
e1 = key.encrypt(Buffer("hello"))
e2 = key.decrypt(e1)

var prefix = '-----BEGIN CERTIFICATE-----\n';
var postfix = '-----END CERTIFICATE-----';
var puKey = prefix + Buffer('1626e57bacbf6d41dc7441f0cf796344d21c8fdb').toString('base64').match(/.{0,64}/g).join('\n') + postfix;
var prKey = prefix + Buffer('f43b06b070f9312ea5a0e8046056194e0f6f381f71c11ce1982c1c5e8e434b52').toString('base64').match(/.{0,64}/g).join('\n') + postfix;
*/

pragma solidity ^0.4.18;

contract Media 		{
	
	uint count = 0;
	address[] public creator_list;

	struct media_c	{
		
		uint media_ID;
		bytes32 creator;
		address creator_add;
		bytes32 url;
		uint256 cost_for_individual;
		uint256 cost_for_company;
		address[] stake_holder_list;
		uint[] stake_list;
	}

	media_c[] media_list;
	mapping (address=>uint) public type_customer;
	
	function Media (address[] cr_add) public  	{
		for (uint j = 0; j < cr_add.length; j++)	{
			if (j % 3 == 0)	{
				creator_list.push(cr_add[j]);
			}
			
			if ( j % 2 == 0)	{
				type_customer[cr_add[j]] = 1; //individual
			}
			else	{
				type_customer[cr_add[j]] = 0; // company
			}
		}
	}


	function validateCreator (address addr) view public returns (bool)	{
		for ( uint i = 0; i < creator_list.length; i++ )	{
			if ( creator_list[i] == addr )		{
				return true;
			}
		}
		return false;
	}

/*
contractInstance.addMedia(1, 'Mahima', web3.eth.accounts[0], 'https://www.mygaana.com', web3.toWei('0.01'), web3.toWei('0.02'),[web3.eth.accounts[1],web3.eth.accounts[2],web3.eth.accounts[3]],[20,20,20], {from: web3.eth.accounts[0], gas:4700000})
contractInstance.addMedia(2, 'Khushboo', web3.eth.accounts[3], 'https://www.mygaana.com', web3.toWei('0.01'), web3.toWei('0.02'),[web3.eth.accounts[3],web3.eth.accounts[4],web3.eth.accounts[5]],[30,30,20], {from: web3.eth.accounts[3], gas:4700000})
*/
	function addMedia(uint ID, bytes32 cr, address cr_add, bytes32 url, uint256 c_i, uint256 c_c, address[] stake_hol_list, uint[] stake_per_list) public {
		require(validateCreator(cr_add));
		require(stake_hol_list.length <= 5);
		require(stake_hol_list.length == stake_per_list.length);
		media_list.push(media_c(ID, cr, cr_add, url, c_i, c_c,stake_hol_list,stake_per_list));
		
		
	}

	//contractInstance.countMedia({from: web3.eth.accounts[0]}).toString()
	function countMedia () public view returns (uint c) {
		return media_list.length;
	}

	//contractInstance.printAllMedia({from: web3.eth.accounts[0]}).toString()
	function printAllMedia () public view returns (uint[], bytes32[]) {
		uint[] temp;
		bytes32[] temp2;
		for (uint i = 0; i < media_list.length; i++)	{
			temp.push( media_list[i].media_ID );
			temp2.push( media_list[i].creator );
		}
		return (temp, temp2);
	}

	function validateAmount(uint cost, uint sent_am) view public returns (bool)		{
		if ( cost == sent_am )	{
			return true;
		}
		return false;
	}

	//Parameters : buyer address, mediaID
/*
contractInstance.buyMedia(web3.eth.accounts[5], 1, {from: web3.eth.accounts[5],value: web3.toWei('0.02','ether') , gas:4700000})
*/
	function buyMedia(address recv_add, uint mID) public payable{
		uint temp = type_customer[recv_add];
		address r_addr;
		uint256 cost;
		uint index_media ; 
		for (uint i = 0; i < media_list.length; i++){
			
			if (media_list[i].media_ID == mID) {
				index_media = i;
				if ( temp == 0 )	{
					cost = media_list[i].cost_for_company;
					r_addr = media_list[i].creator_add;
				}
				else {
					cost = media_list[i].cost_for_individual;
					r_addr = media_list[i].creator_add;
				}
			}
		}
		require(validateAmount(cost,msg.value));
		uint stake_share = 0;
		for (uint s_addr = 0; s_addr < media_list[index_media].stake_holder_list.length;s_addr++){
			media_list[index_media].stake_holder_list[s_addr].transfer(msg.value*media_list[index_media].stake_list[s_addr]/100);
			stake_share += media_list[index_media].stake_list[s_addr];
		}
		r_addr.transfer(msg.value*(100 - stake_share)/100);
	}

	

}