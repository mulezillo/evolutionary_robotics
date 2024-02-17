import os


if __name__ == "__main__":
    # 5 random simulations
    for i in range(5):
        os.system("python3 generate.py")
        os.system("python3 simulate.py")
