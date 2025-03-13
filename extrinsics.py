#!/usr/bin/env python3

import argparse
import bittensor as bt
from bittensor_wallet import Wallet
from scalecodec.base import ScaleBytes
from scalecodec.types import GenericExtrinsic
from typing import Dict, List

subtensor = None


def get_call_args_netuid(call_args: List[Dict]) -> int:
    """
    Get the netuid from the call arguments.

    This is an example of the call_args attribute from an extrinsic:
    'call_args': [
        {'name': 'hotkey', 'type': 'AccountId', 'value': '5F4tQyWrhfGVcNhoqeiNsR6KjD4wMZ2kfhLj4oHYuyHbZAc3'},
        {'name': 'netuid', 'type': 'u16', 'value': 8},
        {'name': 'amount_staked', 'type': 'u64', 'value': 100000000}]

    """
    for arg in call_args:
        if arg.get("name") == "netuid":
            return arg.get("value")
    return None


def retrieve_pending_extrinsics(
    netuid: int,
    network: str = "finney",
    call_functions: List[str] = ["add_stake", "add_stake_limit"],
) -> List[GenericExtrinsic]:
    """
    Retrieve pending extrinsics from the network.

    This was implemented because the substrate interface does not support retrieving pending extrinsics in the current version of bittensor.

    The function filters the results by subnet and call functions. The default values are the ones used in the exercise.

    Args:
        netuid (int): The network UID of the subnet to retrieve extrinsics from. 0 means all subnets.
        network (str): The network to retrieve extrinsics from.
        call_functions (List[str]): The functions to filter extrinsics by.
    Returns:
        List[GenericExtrinsic]: A list of pending extrinsics.
    """
    global subtensor
    # Convenient shortcut to the internal substrate interface
    substrate = subtensor.substrate
    encoded_extrinsics = substrate.rpc_request("author_pendingExtrinsics", [])
    extrinsics = []

    for extrinsic_data in encoded_extrinsics["result"]:
        extrinsic = substrate.create_scale_object(
            "Extrinsic", metadata=substrate.metadata
        )
        extrinsic.decode(
            ScaleBytes(extrinsic_data),
            check_remaining=substrate.config.get("strict_scale_decode"),
        )
        call = extrinsic.value.get("call")
        if call is not None:
            if call.get("call_function") in call_functions:
                # Filter by subnet. 0 means all subnets.
                if netuid == 0 or get_call_args_netuid(call.get("call_args")) == netuid:
                    extrinsics.append(extrinsic)

    return extrinsics


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--netuid",
        type=int,
        help="The network UID of the subnet to retrieve extrinsics from. 0 means all subnets.",
    )
    parser.add_argument(
        "--network",
        type=str,
        default="finney",
        help="The network to retrieve extrinsics from.",
    )
    parser.add_argument(
        "--call_functions",
        type=str,
        default="add_stake,add_stake_limit",
        help="The functions to filter extrinsics by.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    global subtensor
    subtensor = bt.Subtensor(network=args.network)

    pending_extrinsics = retrieve_pending_extrinsics(
        netuid=args.netuid, call_functions=args.call_functions
    )
    # TODO: For this exercise we will use a new wallet. But in a real scenario we would use the wallet we want to stake from.
    wallet = Wallet()
    wallet.create()
    balance = subtensor.get_balance(wallet.coldkey.ss58_address)
    print(f"Balance: {balance}")

    print(f"Found {len(pending_extrinsics)} pending extrinsics")
    for extrinsic in pending_extrinsics:
        subtensor.add_stake(wallet, amount=1)


if __name__ == "__main__":
    main()
