#!/bin/bash

dd if=/dev/urandom bs=1M count=5 | sort | shuf > /dev/null
