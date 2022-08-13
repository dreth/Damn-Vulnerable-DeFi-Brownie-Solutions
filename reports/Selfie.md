## Selfie

### Challenge description

> A new cool lending pool has launched! It's now offering flash loans of DVT tokens.
>
> Wow, and it even includes a really fancy governance mechanism to control it.
>
> What could go wrong, right ?
>
> You start with no DVT tokens in balance, and the pool has 1.5 million. Your objective: take them all.

### Solution

For this challenge, there's a pool offering flash loans and a simple governance contract which has privileges to call functions in the pool contract which are locked by a modifier (`onlyGovernance()`) which require the caller to be the governance contract.

In order to bypass this, we have to be able to propose and execute governance proposals. Anyone can execute a governance proposal in due time if the conditions in `_canBeExecuted()` for a specific `actionId` are met. In this case there's a requirement to wait 2 days after proposing it and before executing it, and the action must not have already been executed (`actionToExecute.executedAt == 0`).

An account is also only allowed to make proposals if it holds at least half of the total supply of the token plus 1 (_yay decentralization?_ or something like that)

After all these requirements are passed, we can call an `onlyGovernance()` gated function called `drainAllFunds()` in SelfiePool, and pass which address we want to send all the funds to.

Given that SelfiePool offers loans in exactly the same token that is required to make governance proposals, I did the following to successfully drain all funds:

1- Deploy an attacker contract which can take loans from the pool:

```cs
function takeLoan() public {
    // execute a flash loan borrowing all available DVT tokens in the pool
    pool.flashLoan(fundsInPool);
}
```

Where `fundsInPool` is a variable set by the constructor of the contract which obtains the entire balance of DVT tokens in the SelfiePool.

The attacker contract must contain a `receiveTokens()` function which takes a snapshot of the token balance:

```cs
token.snapshot();
```

Then queues a governance action with some calldata which executes `drainAllFunds()` with the attacker address as parameter:


```cs
maliciousAction = governance.queueAction(address(pool), attackData, 0);
```

Where `attackData` is such calldata.

After these two actions, the contract should return the borrowed funds back to the pool:

```cs
token.transfer(address(pool), amount);
```

2- After deploying the attacker contract, I generated the calldata for the `drainAllFunds()` function and set it to the `attackData` state variable in the attacker contract.

3- Then called the function in the attacker contract that takes the loan, which executes the actions in `receiveTokens()`, those described in step 1.

4- After this I waited 2 days using the rpc `evm_increaseTime` request (acceptable as it's a testnet environment, in the real world 2 days have to pass)

5- Execute the governance action calling `executeAction()` with the corresponding `actionId`.

This will drain the funds and transfer them to the attacker address.
