'''
    Script compares if both HTTP servers return same final URLS
'''
import logging
import asyncio
import argparse
import aiohttp

parser = argparse.ArgumentParser(description="Script sends request to both HTTP servers with the same path and compares if it returns same URL",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-o", "--output", help="Log output file")
parser.add_argument(
    "pathsfile", help="File containing paths, paths have to be seperated by new line and must start with /")
parser.add_argument("server1", help="sirst Server")
parser.add_argument("server2", help="second Server")

args = parser.parse_args()

config = vars(args)

SERVER1_HOST = config["server1"]
SERVER2_HOST = config["server2"]
PATHS_FILE = config["pathsfile"]
OUTPUT = config["output"]

def read_paths(file):
    '''Reads paths file and returns array of paths'''
    paths_file = open(file, 'r')
    paths = paths_file.readlines()
    paths_file.close()
    return paths


def log(text):
    '''Logs text, if output specified logs to file as well'''
    print(f'{text}\n')
    if (OUTPUT):
        log_file = open(OUTPUT, 'a+')
        log_file.writelines(f'{text}\n')
        log_file.close()


async def send_request(session, host, path):
    '''Sends async request to specified path and returns final path'''
    try:
        async with session.get(f"{host}{path}") as response:
            return str(response.url).replace(host, "")
    except Exception:
        log(f"Failed to send request to {host+path}, error: {logging.critical(Exception, exc_info=True)}")


async def compare_urls(path):
    '''Sends request to each server with same path and checks if final url is the same'''
    async with aiohttp.ClientSession() as session:
        server1_response = await send_request(session, SERVER1_HOST, path)
        server2_response = await send_request(session, SERVER2_HOST, path)
        
        text = ""
        
        if server1_response != server2_response:
            text = (f"{'-'*40} \nRedirection mismatch \n"
                   f"SOURCE = {path}\n"
                   f"{SERVER1_HOST} redirected to = {server1_response}\n"
                   f"{SERVER2_HOST} redirected to = {server2_response}\n"
                   f"{'-'*40}")
        else:
            text = f"Redirection MATCHED! - source: {path}, target: {server1_response}"
            
        log(text)


async def main():
    '''Main script function'''
    paths = read_paths(PATHS_FILE)
    tasks = []

    for path in paths:
        tasks.append(asyncio.create_task(compare_urls(path)))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
