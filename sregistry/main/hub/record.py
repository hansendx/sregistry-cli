'''

Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017-2018 Vanessa Sochat.

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
from sregistry.utils import ( parse_image_name, remove_uri )
import os


def record(self, images, action='add'):
    '''record an image from an endpoint. This function is akin to a pull,
       but without retrieving the image. We only care about the list of images
       (uris) to look up, and then the action that the user wants to take
 
    Parameters
    ==========
    images: refers to the uri given by the user to pull in the format
    <collection>/<namespace>. You should have an API that is able to 
    retrieve metadata for a container based on this url.
    action: the action to take with the record. By default we add it, meaning
            adding a record (metadata and file url) to the database. It is
            recommended to place the URL for the image download under the 
            container.url field, and the metadata (the image manifest) should
            have a selfLink to indicate where it came from.
    '''
    
    if not isinstance(images,list):
        images = [images]

    bot.debug('Execution of RECORD[%s] for %s images' %(action, len(images)))

    for image in images:

        q = parse_image_name(remove_uri(image))

        # Verify image existence, and obtain id
        url = "%s/container/%s/%s:%s" %(self.base, q['collection'], q['image'], q['tag'])
        bot.debug('Retrieving manifest at %s' %url)

        # Get the manifest, add a selfLink to it
        manifest = self._get(url)
        manifest['selfLink'] = url

        image_uri = "%s:%s@%s" %(manifest['name'], manifest['tag'], manifest['version'])
        container = self.add(image_name=image_uri,
                             metadata=manifest,
                             url=manifest['image'])
