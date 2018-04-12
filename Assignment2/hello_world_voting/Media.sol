/* How to run:
code = fs.readFileSync('Media.sol').toString()
solc = require('solc')
compiledCode = solc.compile(code)
abiDefinition = JSON.parse(compiledCode.contracts[':Media'].interface)
VotingContract = web3.eth.contract(abiDefinition)
byteCode = compiledCode.contracts[':Media'].bytecode
deployedContract = VotingContract.new((['0x40a720901d4e971a8947132c6f15f84f69410b15', '0xc749aef1f0dc36ec660ab80280e799c69c07d8e1']), {data: byteCode, from: web3.eth.accounts[0], gas: 4700000})
deployedContract.address
contractInstance = VotingContract.at(deployedContract.address)
contractInstance.addMedia.call(2, 'Mahima', '0x40a720901d4e971a8947132c6f15f84f69410b15', 'https://www.mygaana.com', 12, 32)
contractInstance.addMedia.call(3, 'Mahima', '0x40a720901d4e971a8947132c6f15f84f69410b15', 'https://www.yourgaana.com', 12, 32)
contractInstance.searchMedia(2).toLocaleString()

 */

pragma solidity ^0.4.18;

contract Media 		{

	struct media_c	{
		uint media_ID;
		bytes32 creator;
		address creator_add;
		bytes32 url;
		uint cost_for_individual;
		uint cost_for_company;
	}

	media_c[] mediaList;
	address[] addr_list;
	uint[] media_id;		//creators
	//mapping (media_c=>)

	//deployedContract = VotingContract.new((['0x40a720901d4e971a8947132c6f15f84f69410b15', '0xc749aef1f0dc36ec660ab80280e799c69c07d8e1']), {data: byteCode, from: web3.eth.accounts[0], gas: 4700000})
	function Media (address[] cr_add) public {
		for ( uint i = 0; i < cr_add.length; i++ )	{
			addr_list.push(cr_add[i]);
		}
	}

	//contractInstance.printCreators.call()
	function printCreators () public constant returns (address temp)	{
		//address temp = addr_list[0];
		return addr_list[0];
	}

	//adds media in the mediaList
	//contractInstance.addMedia.call(2, 'Mahima', '0x40a720901d4e971a8947132c6f15f84f69410b15', 'https://www.mygaana.com', 12, 32)
	//contractInstance.addMedia.call(3, 'Mahima', '0x40a720901d4e971a8947132c6f15f84f69410b15', 'https://www.yourgaana.com', 12, 32)
	
	function addMedia (uint ID, bytes32 cr, address cr_add, bytes32 url, uint c_i, uint c_c) public returns (bool) {
		require(validateUser(cr_add));
		mediaList.push(media_c(ID, cr, cr_add,url, c_i, c_c));
		media_id.push(ID);
		return true;
	}
	

	function validateUser (address addr) view public returns (bool)	{
		for ( uint i = 0; i < addr_list.length; i++ )	{
			if ( addr_list[i] == addr )		{
				return true;
			}
		}
		return false;
	}

	function searchMedia (uint id) constant public returns (bool)	{
		
		for ( uint i = 0; i < mediaList.length; i++ )	{
			if ( mediaList[i].media_ID == id )		{
				return true; //should be some id not url since url are added encrypted after the request(khushboo)
			}
		}
		return false;
	}

	function queryallmedia() public constant returns(uint m){
		return media_id.length;
		/*for (uint i = 0; i < mediaList.length; i++)
		{
			//return media_id;
			//searchMedia(mediaList[i].media_ID);
		}*/
	}

	//Added by khushboo
	/*
	function queryallmedia() constant public return	{
		for (uint i=0; i < mediaList.length; i++)
		{
			console.log ("Media:");
		}
	}
	*/
	//added by khushboo
	/*function buy_media() public return(){
	}
	//added by khushboo
	function access_media() return {
		require(pay_media());

	}*/

}
/*'0x40a720901d4e971a8947132c6f15f84f69410b15',
  '0xc749aef1f0dc36ec660ab80280e799c69c07d8e1',
  '0x88da955ce3623dbe9a368c0ba1c127f4fae3fbd9',
  '0x4409aa1d14a04a5c4cc7c032eb2b813caf78b8ea',
  '0x686fd5d082cb3a7b30345247b39c1c98f13fab13',
  '0x44427f5862eaff72520eb44cb94ef423ecf04e23',
  '0x8c93fdb9a4a72f1dcf9e4e8f3499c2a48cacd527',
  '0x3b4c3ab97708a1b59c5c2114bee1be95f6abe90a',
  '0x4db74fd19370308c2796bceabd46ad71ddc1e91b',
  '0x3f04f6c31742c560fcaafe4d9f7d45864b94c488' */
