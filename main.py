import argparse
import re

from first_contact.client import HTBClient
from first_contact.parser import ChallengeParser
from first_contact.orbital import VisibilityCalculator


FLAG_PATTERN = re.compile(r"HTB\{[^}]+\}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="HTB First Contact solver"
    )

    parser.add_argument("host")
    parser.add_argument("port", type=int)

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    client = HTBClient(
        host=args.host,
        port=args.port,
    )

    parser = ChallengeParser()
    calculator = VisibilityCalculator()

    try:
        client.connect()

        challenge_number = 1

        while True:
            response = client.receive_challenge()

            print(response)

            flag = FLAG_PATTERN.search(response)

            if flag:
                print(f"[+] Flag: {flag.group(0)}")
                break

            try:
                challenge = parser.parse(response)
            except ValueError:
                print("[-] No more challenge data found")
                break

            windows = calculator.calculate(challenge)

            answer = " ".join(windows)

            print(
                f"[+] Challenge {challenge_number}: "
                f"{answer}"
            )

            client.send_answer(answer)

            challenge_number += 1

    finally:
        client.close()


if __name__ == "__main__":
    main()