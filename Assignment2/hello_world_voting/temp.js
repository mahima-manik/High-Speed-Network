Web3 = require('web3')
web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

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


const util = require('ethereumjs-util')

const msg = new Buffer('hello');
const sig = web3.eth.sign(web3.eth.accounts[0], '0x' + msg.toString('hex'));
const res = util.fromRpcSig(sig);

const prefix = new Buffer("\x19Ethereum Signed Message:\n");
const prefixedMsg = util.sha3(
  Buffer.concat([prefix, new Buffer(String(msg.length)), msg])
);

const pubKey  = util.ecrecover(prefixedMsg, res.v, res.r, res.s);
const addrBuf = util.pubToAddress(pubKey);
const addr    = util.bufferToHex(addrBuf);

console.log(web3.eth.accounts[0],  addr);

const ecies = require("eth-ecies");

const privateKey = '79ba130044c966ba8df861bd8e882eb95ab9f5ce66e1012e7c44768cbdbdcfcd';
const data = 'www.saavn.com';

let userPublicKey = new Buffer(pubKey, 'hex');
let bufferData = new Buffer(data);
let encryptedData = ecies.encrypt(userPublicKey, bufferData);
const t = encryptedData.toString('base64')
console.log(t);

let userPrivateKey = new Buffer(privateKey, 'hex');
let bufferEncryptedData = new Buffer(encryptedData, 'base64');
let decryptedData = ecies.decrypt(userPrivateKey, bufferEncryptedData);
const y= decryptedData.toString('utf8');
console.log(y);

const msg3 = new Buffer('hello');
const sig3 = web3.eth.sign(web3.eth.accounts[3], '0x' + msg3.toString('hex'));
const res3 = util.fromRpcSig(sig3);

const prefix3 = new Buffer("\x19Ethereum Signed Message:\n");
const prefixedMsg3 = util.sha3(
  Buffer.concat([prefix3, new Buffer(String(msg.length)), msg])
);

const pubKey3  = util.ecrecover(prefixedMsg3, res.v, res.r, res.s);
const addrBuf3 = util.pubToAddress(pubKey3);
const addr3    = util.bufferToHex(addrBuf3);

console.log(web3.eth.accounts[0],  addr3);

const ecies = require("eth-ecies");

const privateKey3 = '79ba130044c966ba8df861bd8e882eb95ab9f5ce66e1012e7c44768cbdbdcfcd';
const data3 = 'www.gaana.com';

let userPublicKey3 = new Buffer(pubKey3, 'hex');
let bufferData3 = new Buffer(data3);
let encryptedData3 = ecies.encrypt(userPublicKey3, bufferData3);

contractInstance.addMedia(1, 'Mahima', web3.eth.accounts[0], encryptedData, web3.toWei('0.01'), web3.toWei('0.02'),[web3.eth.accounts[1],web3.eth.accounts[2],web3.eth.accounts[3]],[20,20,20], {from: web3.eth.accounts[0], gas:4700000})
contractInstance.addMedia(2, 'Khushboo', web3.eth.accounts[3], encryptedData3, web3.toWei('0.01'), web3.toWei('0.02'),[web3.eth.accounts[3],web3.eth.accounts[4],web3.eth.accounts[5]],[30,30,20], {from: web3.eth.accounts[3], gas:4700000})

contractInstance.countMedia({from: web3.eth.accounts[0]}).toString()

web3.fromWei(web3.eth.getBalance(web3.eth.accounts[0])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[5])).toString()

contractInstance.buyMedia(web3.eth.accounts[5], 1, {from: web3.eth.accounts[5],value: web3.toWei('0.02','ether') , gas:4700000})

web3.fromWei(web3.eth.getBalance(web3.eth.accounts[0])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[5])).toString()