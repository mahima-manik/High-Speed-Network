/* How to run:
code = fs.readFileSync('Media.sol').toString()
solc = require('solc')
compiledCode = solc.compile(code)
abiDefinition = JSON.parse(compiledCode.contracts[':Media'].interface)
VotingContract = web3.eth.contract(abiDefinition)
byteCode = compiledCode.contracts[':Media'].bytecode
deployedContract = VotingContract.new(([web3.eth.accounts[0], web3.eth.accounts[1]]), {data: byteCode, from: web3.eth.accounts[0], gas: 4700000})
contractInstance = VotingContract.at(deployedContract.address)
contractInstance.validateUser(web3.eth.accounts[0], {from: web3.eth.accounts[0]})
 */

pragma solidity ^0.4.18;

contract Media 		{
	
	uint count = 0;
	address[] public addr_list;

	struct media_c	{
		uint media_ID;
		bytes32 creator;
		address creator_add;
		bytes32 url;
		uint cost_for_individual;
		uint cost_for_company;
	}

	media_c[] media_list;
	
	//deployedContract = VotingContract.new((['0x40a720901d4e971a8947132c6f15f84f69410b15', '0xc749aef1f0dc36ec660ab80280e799c69c07d8e1']), {data: byteCode, from: web3.eth.accounts[0], gas: 4700000})
	function Media (address[] cr_add) public  {
		for ( uint i = 0; i < cr_add.length; i++ )	{
			addr_list.push(cr_add[i]);
		}
	}


	function validateUser (address addr) view public returns (bool)	{
		for ( uint i = 0; i < addr_list.length; i++ )	{
			if ( addr_list[i] == addr )		{
				return true;
			}
		}
		return false;
	}

	//contractInstance.addMedia(2, 'Mahima', web3.eth.accounts[0], 'https://www.mygaana.com', 12, 32, {from: web3.eth.accounts[0], gas:4700000})
	function addMedia(uint ID, bytes32 cr, address cr_add, bytes32 url, uint c_i, uint c_c) public {
		media_list.push(media_c(ID, cr, cr_add, url, c_i, c_c));
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
}