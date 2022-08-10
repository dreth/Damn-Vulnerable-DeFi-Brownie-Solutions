# Damn Vulnerable DeFi (Brownie Scripts)

This repo is an adaptation of the [Damn Vulnerable DeFi challenges](https://damnvulnerabledefi.xyz) to use Brownie scripts.

Given how unfamiliar (at first) the ethers.js syntax was for me despite knowing some javascript, I decided to adapt the code to work with brownie. In this case, I've basically translated the code for all the challenge setups and success/fail checks to function somewhat similarly to the original challenges.

This was a challenge in itself to familiarize myself a little better with the ethers.js/hardhat syntax and how it works in general by establishing parallels to brownie, which I had become familiarized with through solving the [Ethernaut](https://dac.ac/blog/ethernaut_solutions/) and [Capture the ether](https://dac.ac/blog/capture_the_ether_solutions/) challenges.

This repo can be used by anyone to solve the challenges using brownie scripts, which may be preferred over tests depending on your use of brownie. Given my lack of unit testing experience, scripts feel a little more familiar, that's why I went this route to solve the Ethernaut and Capture the ether challenges. However, given that these challenges are originally written using tests, [I also made a repo like this one to use the brownie testing framework](https://github.com/dreth/DamnVulnerableDeFiBrownie-Tests), the code is pretty much the same, but it uses tests.

I will keep this repo and the repo that uses tests with no solutions, so that anyone can use them.

**If you find an error, please post an issue or open a PR. I would really appreciate it**

## How I set it up

Similar to the original challenges, the user is expected to have a decent idea of what they're doing. So the challenge setup is given right before the code block where the user has to write their actions that will solve a given challenge, as well as the conditions to solve the challenge right under it.

I have also used this approach, but with some little things I like to do when working in brownie to write less code. 

Important details:

* The challenge setup for each challenge is before where you should write the solution in every script under `scripts`, just under `SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE`.

* The setup is largely identical to the original setup, but with some nuances, some related to the development framework (brownie vs ethers+hardhat), others to my personal choices when writing the code for it. I hope my changes make the process easier, but you can always modify what I've done. I won't explain the differences between brownie and ethers+hardhat, but I will explain what things I've changed, and what I haven't:
  
  + **I have not changed variable names**, the signers are called the same as in the original challenges and so are deployed contracts for each challenge
  + The variables `_fromDeployer` or `_fromAttacker` are simply my way of not needing to write `{'from':deployer}` and `{'from':attacker}` respectively. I find this much more comfortable to use and you can use those variables to avoid having to also write the original dictionary version. If you need to send value or data with your tx, just join dictionaries as possible in your python version. I'm using 3.10+, so I usually just use e.g. `_fromAttacker | {'value':100000}` or, as I defined a function to avoid having to also write value dicts: `_fromAttacker | value_dict(100000)`. (_I promise I love dictionaries, but typing them for every tx is rather annoying_)

## How to solve the challenges

The code for each contract is under `contracts`, just like in the original challenges. Any contract's build data for which I needed the ABI and bytecode is under `built_helper_contracts`, you can just ignore this (unless you see a mistake, please notify me if so).

To solve the challenges:

1. Make sure that you can use the hardhat or anvil networks. You'll need to install hardhat or anvil. This is rather easy to do and you can follow the steps outlined in [this article of the brownie docs](https://eth-brownie.readthedocs.io/en/stable/install.html#using-brownie-with-hardhat).

2. Run one of the scripts (or open the brownie console) so that brownie downloads/installs and compiles all required contracts that are required to compile those within the repo. If everything works fine, you don't need to do anything else. For me, however, during compilation, some contracts from the libraries required minimal modifications to work as intended, as a result, I made a simple script in the root directory of the repo (`fix_libs.py`) that will apply those changes to the scripts after brownie installs them.

3. Go under `scripts` to each challenge and write your transactions under the `solve_challenge()` function. Do not modify the code under `SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE`, as those define the initial setup for each challenge.

4. Run each script with:

```
brownie run script_name --network network
```

* `script_name` is the name of your script for each challenge
* `network` after the `--network` flag is either `hardhat` or `anvil`

**Note: If you want to use Anvil, I only managed to get it to work with brownie versions _after_ 1.19.0, as of writing this, that's the latest version of brownie, to implement some fixes that allow Anvil to work well, you should just install [via setuptools while in the master branch of the repo](https://github.com/eth-brownie/brownie#via-setuptools).**

5. The script has several print statements to show each section of each challenge and their respective transactions running. I print those using the `message` function I defined in utils, a rather silly function but I like how the code looks as opposed to just writing print in every script. If your challenge is solved and the assertions all pass, there will be a message that says `Challenge is solved: True`. 

## If you find a mistake

Once again, if you see a mistake in the code, **please open an issue or a PR**. I'm not an expert by any stretch of the imagination and I'm still learning. I wanted to make this so anyone that prefers brownie scripts over ethers+hardhat tests can solve these challenges (including myself), despite this, I still recommend using the original repo to solve the challenges if you can.
