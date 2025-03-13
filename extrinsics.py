#!/usr/bin/env python3

import bittensor as bt
from scalecodec.base import ScaleBytes
from scalecodec.types import GenericExtrinsic
from typing import Dict, List


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
    st = bt.subtensor(network=network)
    # Convenient shortcut to the internal substrate interface
    substrate = st.substrate
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


def main():
    print("Hello from tao-test!")
    pending_extrinsics = retrieve_pending_extrinsics(netuid=0, network="test")

    print(pending_extrinsics)


if __name__ == "__main__":
    main()
