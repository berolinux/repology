#!/usr/bin/env python3
#
# Copyright (C) 2016 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

# mypy: no-disallow-untyped-calls

import unittest

from repology.package import Package, PackageFlags

from .package import spawn_package


class TestParsers(unittest.TestCase):
    def assert_version_compare(self, a: Package, b: Package, res: int) -> None:
        self.assertEqual(a.version_compare(b), res)

    def test_equality(self) -> None:
        self.assertEqual(
            spawn_package(),
            spawn_package()
        )
        self.assertEqual(
            spawn_package(name='a'),
            spawn_package(name='a')
        )

        self.assertNotEqual(
            spawn_package(name='a'),
            spawn_package(name='b')
        )
        self.assertNotEqual(
            spawn_package(),
            spawn_package(name='b')
        )
        self.assertNotEqual(
            spawn_package(name='a'),
            spawn_package()
        )

    def test_flag_p_is_patch(self) -> None:
        self.assert_version_compare(
            spawn_package(version='1.0p1'),
            spawn_package(version='1.0p1'),
            0
        )
        self.assert_version_compare(
            spawn_package(version='1.0p1', flags=PackageFlags.P_IS_PATCH),
            spawn_package(version='1.0p1'),
            1
        )
        self.assert_version_compare(
            spawn_package(version='1.0p1'),
            spawn_package(version='1.0p1', flags=PackageFlags.P_IS_PATCH),
            -1
        )
        self.assert_version_compare(
            spawn_package(version='1.0p1', flags=PackageFlags.P_IS_PATCH),
            spawn_package(version='1.0p1', flags=PackageFlags.P_IS_PATCH),
            0
        )

    def test_flag_outdated(self) -> None:
        self.assert_version_compare(
            spawn_package(version='1.0'),
            spawn_package(version='1.0'),
            0
        )
        self.assert_version_compare(
            spawn_package(version='1.0', flags=PackageFlags.OUTDATED),
            spawn_package(version='1.0'),
            -1
        )
        self.assert_version_compare(
            spawn_package(version='1.0'),
            spawn_package(version='1.0', flags=PackageFlags.OUTDATED),
            1
        )
        self.assert_version_compare(
            spawn_package(version='1.0', flags=PackageFlags.OUTDATED),
            spawn_package(version='1.0', flags=PackageFlags.OUTDATED),
            0
        )

    def test_flag_rolling(self) -> None:
        self.assert_version_compare(
            spawn_package(version='1.0'),
            spawn_package(version='1.0'),
            0
        )
        self.assert_version_compare(
            spawn_package(version='1.0', flags=PackageFlags.ROLLING),
            spawn_package(version='1.0'),
            1
        )
        self.assert_version_compare(
            spawn_package(version='1.0'),
            spawn_package(version='1.0', flags=PackageFlags.ROLLING),
            -1
        )
        self.assert_version_compare(
            spawn_package(version='1.0', flags=PackageFlags.ROLLING),
            spawn_package(version='1.0', flags=PackageFlags.ROLLING),
            0
        )


if __name__ == '__main__':
    unittest.main()
