'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from sregistry.logger import bot
from sregistry.main import ApiConnection
import json
import sys
import os

from .pull import pull
from .add import add
from .query import (
    search, 
    search_all, 
    search_collection
)

base = 'https://www.singularity-hub.org/api'

class Client(ApiConnection):


    def __init__(self, secrets=None, base=None, **kwargs):
 
        self.base = base
        self.update_base() 
        self.update_headers()
        super(ApiConnection, self).__init__(**kwargs)

    def update_base(self, new_base=None):

        if new_base is None:
            new_base = base
        self.base = new_base

        if self.base is not None:
            if not self.base.endswith('api'):
                self.base = '%s/api' %self.base.strip('/')

    

Client.pull = pull
Client.search = search
Client.add = add
Client._search_all = search_all
Client._search_collection = search_collection
