var Web3 = require('web3')
const solc = require('solc')
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
const fs = require('fs')
var code = fs.readFileSync('Media.sol').toString()

var compiledCode = solc.compile(code)
var abiDefinition = JSON.parse(compiledCode.contracts[':Media'].interface)
var VotingContract = web3.eth.contract(abiDefinition)
var byteCode = '0x' + compiledCode.contracts[':Media'].bytecode
var deployedContract = VotingContract.new((web3.eth.accounts), {data: byteCode, from: web3.eth.accounts[0], gas: 4700000})
var contractInstance = VotingContract.at(deployedContract.address)
let temp = contractInstance.validateCreator(web3.eth.accounts[0])
console.log("Reached", temp)
/*
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[0])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[1])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[2])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[3])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[4])).toString()


const util = require('ethereumjs-util')
const ecies = require("eth-ecies");

const url_buff = new Buffer('www.saavn.com');
const sig0 = web3.eth.sign(web3.eth.accounts[0], '0x' + url_buff.toString('hex'));
const res0 = util.fromRpcSig(sig0);
const prefix = new Buffer("\x19Ethereum Signed Message:\n");
const prefixedMsg = util.sha3(
  Buffer.concat([prefix, new Buffer(String(msg.length)), msg])
);
const pubKey0  = util.ecrecover(prefixedMsg, res.v, res.r, res.s);

const addrBuf0 = util.pubToAddress(pubKey0);
const addr = util.bufferToHex(addrBuf0);    //just to match that the address obtained from the public key is the same
console.log(web3.eth.accounts[0],  addr);

privateKey0 = '1ab548f405d6b68af8cfd64eee7cea0cc3a149cd1e76ef5d8b4e9334e525558a';

let pubKey0_buff = new Buffer(pubKey0, 'hex');
let url_m1_buff = new Buffer(url_m1);
let url_m1_enc = ecies.encrypt(pubKey0_buff, url_m1_buff);
const url_m1_enc_str = url_m1_enc.toString('base64')
console.log(url_m1_enc_str);

let PrivateKey0_buff = new Buffer(privateKey0, 'hex');
let url_m1_enc_buff = new Buffer(url_m1_enc, 'base64');
let url_m1_dec = ecies.decrypt(PrivateKey0_buff, url_m1_enc_buff);
const y = url_m1_dec.toString('utf8');
console.log(y);

const msg3 = new Buffer('hello');
const sig3 = web3.eth.sign(web3.eth.accounts[3], '0x' + msg3.toString('hex'));
const res3 = util.fromRpcSig(sig3);

const prefix3 = new Buffer("\x19Ethereum Signed Message:\n");
const prefixedMsg3 = util.sha3(
  Buffer.concat([prefix3, new Buffer(String(msg3.length)), msg3])
);

const pubKey3  = util.ecrecover(prefixedMsg3, res3.v, res3.r, res3.s);
const addrBuf3 = util.pubToAddress(pubKey3);
const addr3    = util.bufferToHex(addrBuf3);

console.log(web3.eth.accounts[0],  addr3);

//const ecies = require("eth-ecies");

const privateKey3 = '79ba130044c966ba8df861bd8e882eb95ab9f5ce66e1012e7c44768cbdbdcfcd';
const data3 = 'www.gaana.com';

let userPublicKey3 = new Buffer(pubKey3, 'hex');
let bufferData3 = new Buffer(data3);
let encryptedData3 = ecies.encrypt(userPublicKey3, bufferData3);

contractInstance.addMedia(1, 'Mahima', web3.eth.accounts[0], encryptedData.toString(), web3.toWei('0.01'), web3.toWei('0.02'),[web3.eth.accounts[1],web3.eth.accounts[2],web3.eth.accounts[3]],[20,20,20], {from: web3.eth.accounts[0], gas:4700000})
contractInstance.addMedia(2, 'Khushboo', web3.eth.accounts[3], encryptedData3.toString(), web3.toWei('0.01'), web3.toWei('0.02'),[web3.eth.accounts[3],web3.eth.accounts[4],web3.eth.accounts[5]],[30,30,20], {from: web3.eth.accounts[3], gas:4700000})

contractInstance.countMedia({from: web3.eth.accounts[0]}).toString()

web3.fromWei(web3.eth.getBalance(web3.eth.accounts[0])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[5])).toString()

contractInstance.buyMedia(web3.eth.accounts[5], 1, {from: web3.eth.accounts[5],value: web3.toWei('0.02','ether') , gas:4700000})

web3.fromWei(web3.eth.getBalance(web3.eth.accounts[0])).toString()
web3.fromWei(web3.eth.getBalance(web3.eth.accounts[5])).toString()
*/