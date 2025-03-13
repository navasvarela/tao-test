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
