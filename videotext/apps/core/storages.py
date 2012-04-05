import os
from datetime import datetime
from io import BufferedWriter, FileIO
from multiprocessing import Pool
from StringIO import StringIO
import boto
from django.conf import settings

from ajaxuploader.backends.base import AbstractUploadBackend
from ajaxuploader.backends.s3 import S3UploadBackend

'''
For some reason no matter what I do the uploaded file size ends up being 0-bytes. The key gets created and chunks are added, but something happens
where they don't reach S3. I'm going to update this to first throw it into local storage and then push it to S3 after the upload is complete. May
take longer, but I think it'll work.

Much borrowed from here: https://github.com/pandaproject/panda/blob/master/panda/storage.py
'''
class TVNS3UploadBackend(AbstractUploadBackend):
    
    
    def update_filename(self, request, filename):
        """
        Verify that the filename is unique, if it isn't append and iterate
        a counter until it is.
        """
        self._original_filename = filename

        filename = self._original_filename
        root, ext = os.path.splitext(self._original_filename)
        path = os.path.join('/tmp/', filename)

        i = 1

        while os.path.exists(path):
            filename = '%s%i%s' % (root, i, ext)
            path = os.path.join('/tmp/', filename)
            i += 1

        return filename 
    
    
    def upload_chunk(self, chunk):
        """
        Write a chunk of data to the destination.
        """
        self._dest.write(chunk)


    def setup(self, filename):
        """
        Open the destination file for writing.
        """
        self._path = os.path.join('/tmp/', filename)

        try:
            os.makedirs(os.path.realpath(os.path.dirname(self._path)))
        except:
            pass

        self._dest = BufferedWriter(FileIO(self._path, "w"))
        
        self._bucket = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                                       settings.AWS_SECRET_ACCESS_KEY)\
                            .lookup(settings.AWS_STORAGE_BUCKET_NAME)
        
        
    def upload_complete(self, request, filename):
        #file is written, go ahead and close it and open for reading.
        self._dest.close()
        file = open(self._path)
        #generate an S3 key
        self._s3_name = '{0}{1}/{2}'.format(settings.AWS_UPLOAD_FOLDER, request.user.username, filename)
        #and see if it exists
        self._s3_key = self._bucket.get_key(self._s3_name)
        #if it doesn't exist, we're good to go, just create it and move on.
        if not self._s3_key:
            self._s3_key = self._bucket.new_key(self._s3_name)
        #if it does exist, we'll want to create a different one so the existing one isn't nuked.
        else:
            #just use utc time to create a prefix.
            self._s3_name = '{0}{1}/{2}-{3}'.format(settings.AWS_UPLOAD_FOLDER, request.user.username, datetime.now().strftime('%m-%d-%Y-%H-%M-%S'), filename)
            self._s3_key = self._bucket.new_key(self._s3_name)
        #send the contents
        self._s3_key.set_contents_from_file(file)
        #make sure it's public
        self._s3_key.set_acl("public-read")
        #close the file
        file.close()
        #delete the file from the server.
        os.remove(self._path)
        #and return the file location.
        return {"path": 'http://{0}{1}'.format(settings.AWS_STORAGE_BUCKET_NAME, self._s3_name)}
    
        
'''

def update_filename(self, request, filename):
    filename = '{0}{1}/{2}'.format(settings.AWS_UPLOAD_FOLDER, request.user.username, filename)
    return filename
    
def upload_chunk(self, chunk):
        self._counter += 1
        buffer = StringIO()
        buffer.write(chunk)
        self._pool.apply_async(
            self._mp.upload_part_from_file(buffer, self._counter))
        buffer.close()

def setup(self, filename):
        self._bucket = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                                       settings.AWS_SECRET_ACCESS_KEY, is_secure = False)\
                            .lookup(settings.AWS_STORAGE_BUCKET_NAME)
        #So on S3 files ARE the entire path, not folders. So make our filename have the appropriate path.
        self._mp = self._bucket.initiate_multipart_upload(filename)
        self._pool = Pool(processes=self.NUM_PARALLEL_PROCESSES)
        self._counter = 0

def upload_complete(self, request, filename):
        super(TVNS3UploadBackend, self).upload_complete(request, filename)
        
        s3_file = self._bucket.get_key(filename)
        s3_file.set_acl("public-read")
        
        
        return {"path": 'http://{0}{1}'.format(settings.AWS_STORAGE_BUCKET_NAME, filename)}

'''
