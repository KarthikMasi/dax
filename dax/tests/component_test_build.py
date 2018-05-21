
from unittest import TestCase

import StringIO
import json
import yaml
import xml.etree.cElementTree as xmlet
import itertools


from dax import XnatUtils
from dax.tests import unit_test_common_processor_yamls as yamls
from dax.tests.common_session_tools import SessionTools
from dax.yaml_doc import YamlDoc
from dax import AutoProcessor


# TODO: BenM/xnat refactor/ these sanity checks should be refactored into
# integration tests and performed on a test database that is explicitly
# setup / torn down within the scope of a test suite execution.
# Remove everything that doesn't make it into an integration test _before_
# the pull request back to vuiis/dax!

host = 'http://10.1.1.17'
proj_id = 'testproj1'
subj_id = 'subj1'
sess_id = 'sess1'
scan_id = '1'
assr_id = 'asr1'

asrxsitype = 'proc:genProcData'
scanxsitype = 'xnat:mrScanData'

expstr = '/data/projects/{}/subjects/{}/experiments/{}'.format(
    proj_id, subj_id, sess_id)
scanstr = '/scans/{}'


# test dimensions:
#
# usable - processor:
# not set, false, true
#
# usable - scan / assessor:
# (unusable, questionable, usable, preferred), various
#
# types - scan / assessor:
# (1 type, several types), 1 type?
#
# needs qc - processor
# not set, false, true
#
# required - resource
# not set, false, true
#
#
# qc status - assessor
# JOB_PENDING, NEEDS_QA, GOOD, PASSED_QA, FAILED, BAD, POOR, RERUN, REPROC
# DONOTRUN, FAILED_NEEDS_REPROC, PASSED_EDITED_QA,
# OPEN_QA_LIST(RERUN, REPROC), BAD_QA_STATUS(FAILED, BAD, POOR, DONOTRUN)
#
# job status - assessor
# NO_DATA, NEED_TO_RUN, NEED_INPUTS, JOB_RUNNING, JOB_FAILED,
# READY_TO_UPLOAD, UPLOADING, COMPLETE, READY_TO_COMPLETE, DOES_NOT_EXIST,
# OPEN_STATUS_LIST(NEED_TO_RUN, UPLOADING, JOB_RUNNING, READY_TO_COMPLETE,
# JOB_FAILED), JOB_BUILT
#
# inputs
# no scans, 1 scan, n scans
# no assessors, 1 assessor, n assessors
# zero variables, one variable, n variables (from an input)
#
# select
# not set, foreach, foreach(other), one, some, all



class ComponentTestBuild(TestCase):

    asrxsitype = 'proc:genProcData'
    scanxsitype = 'xnat:mrScanData'

    expstr = '/data/projects/{}/subjects/{}/experiments/{}'.format(
        proj_id, subj_id, sess_id)
    scanstr = '/scans/{}'


    scan1_yaml = yamls.generate_yaml(
        scans=[
            {
                'name': 'scan1', 'types': 'T1', 'select': None, 'qc': None,
                'resources': [
                    {'type': 'NIFTI', 'name': 't1', 'required': None}
                ]
            }
        ]
    )

    @staticmethod
    def __generate_yamls(entries):
        yamldocs = []
        for e in entries:
            print e
            yamldocs.append(
                yamls.generate_yaml(
                    scans=[{
                        'name': 'scan1',
                        'types': 'T1',
                        'select': e['select'],
                        'qc': e['quality'],
                        'resources': [{
                            'type': 'NIFTI',
                            'name': 't1',
                            'required': e['required']
                        }]
                    }]
                )
            )

    @staticmethod
    def __setup_session(session, parameters):
        intf = session._intf
        #__add_scan()




    def test_build_matrix(self):

        input_headers = ['xsitype', 'quality', 'type', 'files']
        input_xsitype = ['xnat:mrScanData']
        input_quality = ['unusable', 'usable', 'preferred']
        input_type = ['T1', 'T2']
        input_files = [
            [],
            [('NIFTI', ['images.nii'])],
            #[('NIFTI', ['images.nii']), ('SNAPSHOTS', ['snapshot.jpg.gz', 'snapshot(1).jpg.gz'])]
        ]
        input_values = [input_xsitype, input_quality, input_type, input_files]
        input_table_values = itertools.product(*input_values)
        input_table = map(lambda r: [dict(itertools.izip(input_headers, r))],
                          input_table_values)

        headers = ['required', 'select', 'quality', 'inputs']
        required = [None, False, True]
        select = [None, 'foreach']
        quality = [None, False, True]
        input_fields = [[]] + [i for i in input_table]
        values = [required, select, quality, input_fields]
        table_values = itertools.product(*values)
        table = map(lambda r: dict(itertools.izip(headers, r)), table_values)

        # generate the scan artefacts against which this is run
        for scans in input_table:
            for scan in scans:
                SessionTools.add_scan(None, 'scan1', scan)


        print len(table)
