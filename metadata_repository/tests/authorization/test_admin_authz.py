# Big Data Smart Socket
# Copyright (C) 2016 Clemson University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import unittest

from .base import BaseAuthorizationTestMixin


class TestAdminAuthorization(BaseAuthorizationTestMixin, unittest.TestCase):

    def login(self):
        self.loginAdmin()

    def forbiddenEndpoints(self):
        return []

    def okEndpoints(self):
        return [
            ("auth.login", "GET"),
            ("auth.login", "POST"),
            ("auth.register", "GET"),
            ("auth.register", "POST"),
            ("auth.logout", "GET"),

            ("configuration.export_configuration", "GET"),
            ("configuration.import_configuration", "GET"),
            ("configuration.import_configuration", "POST"),
            ("configuration.index", "GET"),

            ("core.index", "GET"),
            ("core.transfers", "GET"),
            ("core.transfers", "POST"),

            ("data_sources.create_data_source", "GET"),
            ("data_sources.create_data_source", "POST"),
            ("data_sources.data_source_relations", "GET"),
            ("data_sources.delete_data_source", "GET"),
            ("data_sources.delete_data_source", "POST"),
            ("data_sources.edit_data_source", "GET"),
            ("data_sources.edit_data_source", "POST"),
            ("data_sources.list_data_sources", "GET"),
            ("data_sources.search_data_sources", "GET"),
            ("data_sources.show_data_source", "GET"),
            ("data_sources.show_transfer_mechanism_options_form", "GET"),
            ("data_sources.test_data_source_url_match", "GET"),
            ("data_sources.test_data_source_url_match", "POST"),

            ("destinations.create_destination", "GET"),
            ("destinations.create_destination", "POST"),
            ("destinations.delete_destination", "GET"),
            ("destinations.delete_destination", "POST"),
            ("destinations.edit_destination", "GET"),
            ("destinations.edit_destination", "POST"),
            ("destinations.list_destinations", "GET"),
            ("destinations.show_destination", "GET"),

            ("matchers.add_url_matcher", "GET"),
            ("matchers.add_url_matcher", "POST"),
            ("matchers.delete_url_matcher", "GET"),
            ("matchers.delete_url_matcher", "POST"),
            ("matchers.edit_url_matcher", "GET"),
            ("matchers.edit_url_matcher", "POST"),
            ("matchers.list_url_matchers", "GET"),
            ("matchers.show_matcher_options_form", "GET"),
            ("matchers.show_url_matcher", "GET"),

            ("static", "GET"),

            ("test_files.add_test_file", "GET"),
            ("test_files.add_test_file", "POST"),
            ("test_files.delete_test_file", "GET"),
            ("test_files.delete_test_file", "POST"),
            ("test_files.edit_test_file", "GET"),
            ("test_files.edit_test_file", "POST"),
            ("test_files.list_test_files", "GET"),
            ("test_files.show_test_file", "GET"),

            ("transfer_reports.delete_transfer_report", "GET"),
            ("transfer_reports.delete_transfer_report", "POST"),
            ("transfer_reports.list_transfer_reports", "GET"),
            ("transfer_reports.report_transfer", "POST"),
            ("transfer_reports.show_transfer_report", "GET"),
            ("transfer_reports.transfer_reports_graph", "GET"),

            ("transforms.add_transform", "GET"),
            ("transforms.add_transform", "POST"),
            ("transforms.delete_transform", "GET"),
            ("transforms.delete_transform", "POST"),
            ("transforms.edit_transform_order", "GET"),
            ("transforms.edit_transform", "GET"),
            ("transforms.edit_transform", "POST"),
            ("transforms.show_transform", "GET"),
            ("transforms.show_transform_options_form", "GET"),

            ("users.edit_user_permissions", "GET"),
            ("users.edit_user_permissions", "POST"),
            ("users.list_users", "GET"),
            ("users.show_user", "GET"),
        ]

    def unauthorizedEndpoints(self):
        return []
