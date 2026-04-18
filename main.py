import sys
from src.config import Config
from src.orchestrator import BOMAutomation

def main():
    config = Config()
    config.load()
    config.parse_args()
    
    automation = BOMAutomation(config)
    try:
        automation.run()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Exiting safely.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[!] Fatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
