#!/bin/bash
git clone --no-checkout "$1"
cd "$2"
git sparse-checkout init --cone
git sparse-checkout set "$3"
git checkout "$4"