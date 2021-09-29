// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.0;

contract SimpleStorage {
    // uint256 favNumber = 5; // unsigned int
    // bool favBool = true;
    // string favString = 'string';
    // int256 favInt = -5;   // signed int
    // address favAddress = 0x015Eb143584DfdD38D4605c73D601F41d02525Cf;
    // bytes32 favBytes = 'cat';
    
    
    // this will initialize to 0
    uint256 favNumber;
    
    struct People {
        uint256 favNumber;
        string name;
    }
    
    People[] public people;
    mapping(string => uint256) public nameToFavNumber;
    
    function store (uint256 _favNumber) public {
        favNumber = _favNumber;
    }
    
    // view, pure (needed if doing some math)
    function retrieve() public view returns(uint256) {
        return favNumber;
    }
    
    function addPerson(string memory _name, uint256 _favNumber) public {
        people.push(People(_favNumber, _name));
        nameToFavNumber[_name] = _favNumber;
    }
}