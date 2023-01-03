// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.6.0;

/// @title simple storage.

contract smartStorage {
    //This will initilized to 0!
    uint256 public favoriteNumber = 666;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    mapping(string => uint256) public nameToFavoriteNumber;
    mapping(uint256 => string) public favoriteNumbeToName;

    //People public person = People({favoriteNumber:2, name:"Paul"});
    //declare an array named people with People type
    People[] public people;

    //This function will change de value of favoriteNumber variable
    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return _favoriteNumber;
    }

    //keyword view and pure are non-state changing functions
    //view read the state of the blockchain
    //pure function that do mathematics
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    //storage and memory
    //memory : delete variable after execution
    //storage : keet it forever
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        //People.push(People({favoriteNumber : _favoriteNumber, name : _name}));
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
        favoriteNumbeToName[_favoriteNumber] = _name;
    }
}
