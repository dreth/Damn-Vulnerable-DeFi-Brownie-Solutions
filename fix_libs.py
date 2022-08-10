import os

# contracts without license, to avoid compiler complaints
files_to_add_license_to = {
    'IUniswapV2Pair.sol':'.brownie/packages/Uniswap/v2-core@1.0.1/contracts/interfaces/',
    'UniswapV2Library.sol':'.brownie/packages/Uniswap/v2-periphery@1.0.0-beta.0/contracts/libraries/'}

for contract, path in files_to_add_license_to.items():
    with open(f'/home/{os.environ["USER"]}/{path}/{contract}','r') as f:
        contents = f.read()
        first_line = contents.splitlines()[0]

    with open(f'/home/{os.environ["USER"]}/{path}/{contract}','w') as f:
        if '// SPDX-License-Identifier: GPL-v3.0' not in first_line:
            f.truncate(0)
            f.write(f'// SPDX-License-Identifier: GPL-v3.0\n{contents}')
        else:
            f.write(contents)


# files with solidity pragma statement that makes the compiler complain
files_with_pragma_statement_to_fix = {
    'SafeMath.sol':'.brownie/packages/Uniswap/v2-periphery@1.0.0-beta.0/contracts/libraries/'
}

versions_found = {
    'pragma solidity =0.6.6;':'pragma solidity >=0.6.6 <0.9.0;'
}

for contract, path in files_with_pragma_statement_to_fix.items():
    with open(f'/home/{os.environ["USER"]}/{path}/{contract}','r') as f:
        contents = f.read()

for contract, path in files_with_pragma_statement_to_fix.items():
    with open(f'/home/{os.environ["USER"]}/{path}/{contract}','w') as f:
        for line in contents.splitlines():
            for statement, fixed_statement in versions_found.items():
                if statement in line:
                    contents = contents.replace(statement, fixed_statement)
        f.write(contents)
