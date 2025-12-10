import time

from modules.utils import print_header, get_int_input, pause


def countdown_timer():
    """Simple countdown timer in seconds."""
    print_header("COUNTDOWN TIMER")
    seconds = get_int_input("Enter time in seconds: ", min_value=1)

    for remaining in range(seconds, 0, -1):
        print(f"\rTime remaining: {remaining} seconds", end="")
        time.sleep(1)

    print("\rTime remaining: 0 seconds          ")
    print("\n⏰ Time's up!")
    pause()


def stopwatch():
    """Stopwatch that shows live running time. Stop with Ctrl+C."""
    print_header("STOPWATCH")
    print("Press Enter to start the stopwatch.")
    input()
    start = time.time()
    print("Stopwatch running... Press Ctrl+C to stop.")

    try:
        while True:
            elapsed = time.time() - start
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            millis = int((elapsed - int(elapsed)) * 100)

            # \r se same line update hoti rahegi
            print(f"\rElapsed time: {minutes:02d}:{seconds:02d}.{millis:02d}", end="")
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Jab tum Ctrl+C dabaoge, yahan aayega
        end = time.time()
        elapsed = end - start
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        millis = int((elapsed - int(elapsed)) * 100)

        print(f"\n\nFinal time: {minutes:02d}:{seconds:02d}.{millis:02d}")
        pause()


def run_timer():
    """Run the timer & stopwatch menu."""
    while True:
        print_header("TIMER & STOPWATCH")
        print("1. Countdown Timer")
        print("2. Stopwatch")
        print("3. Back to Main Menu")
        print()

        choice = get_int_input("Enter your choice (1-3): ", min_value=1, max_value=3)

        if choice == 1:
            countdown_timer()
        elif choice == 2:
            stopwatch()
        elif choice == 3:
            break
