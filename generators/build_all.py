#!/usr/bin/env python3
"""
build_all.py → régénère tous les visuels de assets/ d'un coup.

    python generators/build_all.py            # tous les assets statiques
    python generators/build_all.py --stats    # + dist/telemetry.svg en données fictives (aperçu)

Un script par asset (chacun se lance aussi seul) :
    hero.py               → assets/hero.svg
    sections.py           → assets/section-01..05.svg
    identity.py           → assets/identity.svg
    stack.py              → assets/stack.svg
    mission_cetud.py      → assets/mission-01.svg
    mission_jwt.py        → assets/mission-02.svg
    mission_portfolio.py  → assets/mission-03.svg
    uplinks.py            → assets/uplink-*.svg
    footer.py             → assets/footer.svg
    telemetry.py          → dist/telemetry.svg (lancé par la GitHub Action)
"""
import sys

import footer
import hero
import identity
import mission_cetud
import mission_jwt
import mission_portfolio
import sections
import stack
import uplinks


def main():
    hero.main([])
    sections.main([])
    identity.main()
    stack.main()
    mission_cetud.main()
    mission_jwt.main()
    mission_portfolio.main()
    uplinks.main([])
    footer.main()
    if "--stats" in sys.argv:
        sys.argv.append("--mock")
        import telemetry
        telemetry.MOCK = True
        telemetry.main()


if __name__ == "__main__":
    main()
