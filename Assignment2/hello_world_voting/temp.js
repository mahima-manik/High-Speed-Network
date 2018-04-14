Web3 = require('web3')
web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

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
const data = 'hello';

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
