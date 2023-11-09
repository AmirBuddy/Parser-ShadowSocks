# ss-base64-parser

This is a Python script that helps you generate a configuration file for Shadowsocks proxies. It takes a file called `shadowsocks.txt` as input, which contains a list of Shadowsocks links. The script parses each link and extracts the necessary information (encryption method, password, IP address, and port) to create a configuration file called `config.conf`.

## Prerequisites
- Python 3.x

## Usage
1. Place your Shadowsocks links in a file called `shadowsocks.txt`, with each link on a separate line.
2. Run the script using the command `python script.py`.
3. The script will generate a configuration file named `config.conf` in the same directory.

## Configuration File Format
The generated `config.conf` file follows the format accepted by Shadowsocks clients. It includes a `[General]` section with some default settings and a `[Proxy]` section that lists the configured proxies. Additionally, a `[Proxy Group]` section is created with a group named `SelectGroup` that includes all the configured proxies.

## Note
- Make sure you have the necessary permissions to read `shadowsocks.txt` and write to `config.conf`.
- The script assumes that the Shadowsocks links in `shadowsocks.txt` are valid and correctly formatted. Invalid links may result in errors or unexpected behavior.

Feel free to modify the script to suit your specific needs or integrate it into your existing workflow.
