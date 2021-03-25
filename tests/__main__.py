import doctest
import composable

print('Testing..')

results = doctest.testmod(composable.base)

if results.attempted:
    if results.failed:
        print('Failure!')
    else:
        print('Success!')
else:
    print('No tests found!')
