/* How to run:
code = fs.readFileSync('Media.sol').toString()
solc = require('solc')
compiledCode = solc.compile(code)
abiDefinition = JSON.parse(compiledCode.contracts[':Media'].interface)
VotingContract = web3.eth.contract(abiDefinition)
byteCode = compiledCode.contracts[':Media'].bytecode
deployedContract = VotingContract.new((['0x8b242c3ff88f4e5d9f5f7c2354e18f3dd5c832af',  '0xdd88c8df89079b201c43f7085080fdd3f03ea882']), {data: byteCode, from: web3.eth.accounts[0], gas: 4700000})
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
	uint count = 0;
	media_c[] public mediaList;
	address[] public addr_list;
	uint[] public media_id;		//creators
	//mapping (media_c=>)

	//deployedContract = VotingContract.new((['0x40a720901d4e971a8947132c6f15f84f69410b15', '0xc749aef1f0dc36ec660ab80280e799c69c07d8e1']), {data: byteCode, from: web3.eth.accounts[0], gas: 4700000})
	function Media (address[] cr_add) public  {
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
	
	function addMedia (uint ID, bytes32 cr, address cr_add, bytes32 url, uint c_i, uint c_c) public returns (uint c) {
		require(validateUser(cr_add));

		mediaList.length = mediaList.length +1;
		// mediaList.push(media_c(ID, cr, cr_add,url, c_i, c_c));
		// media_id.push(ID);
		return mediaList.length;
	}
	function getMediaCount() view public returns (uint)
	{
		return mediaList.length;
	}

	function validateUser (address addr) view public returns (bool)	{
		for ( uint i = 0; i < addr_list.length; i++ )	{
			if ( addr_list[i] == addr )		{
				return true;
			}
		}
		return false;
	}

	function printM (uint i) public returns (bytes32 c)	{
		//address temp = addr_list[0];
		return mediaList[i].creator;
	}

	function searchMedia (uint id) public returns (bool)	{
		
		for ( uint i = 0; i < mediaList.length; i++ )	{
			if ( mediaList[i].media_ID == id )		{
				
				return true; //should be some id not url since url are added encrypted after the request(khushboo)
			}
			printM (i);
		}
		return false;
	}

	/*function queryallmedia() constant public returns (media_c m){
		return 
		/*for (uint i = 0; i < mediaList.length; i++)
		{
			//return media_id;
			//searchMedia(mediaList[i].media_ID);
		}
}*/

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
/*
[ '0x8b242c3ff88f4e5d9f5f7c2354e18f3dd5c832af',
  '0xdd88c8df89079b201c43f7085080fdd3f03ea882',
  '0x499720f63cbc7414f3b6fea9f26683381b22a4fa',
  '0xd8d7fc1067ec74fbc385f8afbf8dc1ffcf647a7c',
  '0x3c5e394f2f1e904ad2995f9a0a7d49232b40d9e6',
  '0x17fdf4e2bf6152f7141e911ce4f90ece22a30bcf',
  '0xfb257934afe065693bd7bb7e9d8c1cb7d60f755a',
  '0x1dba5a921012721078dfd07fbcc67a098c0e1bc2',
  '0x77efb2cbaccf3f12293a4f6820357c5b4cb8ca2c',
  '0x4beac242f22c9fddb22a8901efd023a1854f3247' ]
 */
