
pragma solidity ^0.4.18;
// We have to specify what version of compiler this code will compile with

contract User {
    bytes32 userid;
    bytes32 username;
    bool isCreator;

    function User(bytes32 uid, bytes32 uname, bool isc) public {
        userid = uid;
        username = uname;
        isCreator = isc;
    }

    function get() public constant returns (bytes32 u) {
        u = username;
    }
}