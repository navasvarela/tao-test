# Extrinsics exercise

Using inspiration from this article: https://coldint.io/hello-world/, create a script that checks the pending extrinsics for add_stake or add_stake_limit on subnet 4.
Then if an extrinsic is found, create your own add_stake extrinsic that would buy 1 tao worth of subnet 4 token and have it be submitted on the same block that you found the pending extrinsic on.

## Installation and usage

I used [uv](https://docs.astral.sh/uv/) as the package manager. To install the project dependencies, simply run `uv install`.

The implementation of the exercise is in the script is called [`extrinsics.py`]. To execute it, simply `python extrinsics.py` or `./extrinsics.py`.

## Implementation notes

I used bittensor SDK for the exercise. The current version has different implementation from the version used in the article. `SubstrateInterface` has a different implementation because
`bittensor` uses a different library for substrate. The main impact is that `retrieve_pending_extrinsics` is not implemented anymore. Therefore I implemented my own version based on the legacy implementation.
I added some custom arguments that allow filtering extrinsics by call functions and subnet as it is required by the exercise.

The next step is to buy 1 tao worth of tokens and submit it to the same block where the pending extrinsic is found. I've done my best effor but I feel I need to learn more about bittensor to complete the task. I'll describe my limitations
here.

First we need a wallet. I implemented the creation and use of a default wallet but ideally we should allow the user to provide its own wallet. I wasn't able to find good APIs to do this.

I could not find where to get test tokens to fund the wallet. I saw some instructions about connecting to a discord. I did that, and it pointed to a non-existing channel.

I wasn't sure how to buy and submit the explicit to the same block. I spent some time looking at the Bittensor SDK APIs and couldn't find a good example. I went for `subtensor.add_stake(wallet, amount=1)`, which I'm not sure it does what it should. I wasn't able to get a succesful stake because of lack of funds or perhaps another error.

Also I did not write any unit tests. I prioritised moving forward with the algorithm and completing a first implementation quickly.
