# -*- coding: utf-8 -*-

from ...common.api import BaseAPITask


class ProviderResponseAPITask(BaseAPITask):

    def __init__(self):
        """
        """
        super().__init__()

        self.chg_file   =   None
        self.frn        =   None
    

    def get_challenge_ids( self, filename, column='challenge_id', dffilter=None ):
        """
        """
        import pandas as pd
        from pathlib import Path

        assert Path(filename).is_file()

        suffix      =   Path(filename).suffix.lower()

        if suffix == '.csv':
            self.logger.info('Reading CSV input -- column:%s filename:%s', column, Path(filename))
            df      =   pd.read_csv(filename, dtype={ column: int })
        elif suffix in [ '.xls', '.xlsx' ]:
            self.logger.info('Reading Excel input -- column:%s filename:%s', column, Path(filename))
            df      =   pd.read_excel(filename, dtype={ column: int })
        
        if callable(dffilter):
            df      =   df.loc[dffilter(df)]

        if df.empty:
            self.logger.error('No values detected')
            raise ValueError
        
        self.logger.info('Read %s values from column:%s (%s ...)', len(df), column, ', '.join(df[column][:5].values.astype(str)))
        
        return df[column].astype(str).values.tolist()
    

    def upload_bulk_document(self, filename, **kwargs ):
        """
        """
        from pathlib import Path

        assert Path(filename).is_file()
        assert self.args['response_type_code'] in [ 1, 2, 3, 4 ]

        method          =   'POST'
        apipath         =   '/api/vendor/submission/crowdsource/bulk/uploadSupportingDocuments/{frn}/{type}'.format(
                                frn=str(int(self.frn)).zfill(10),
                                type=self.args['response_type_code']
                            )
        content_type    =   'multipart/form-data'

        self.logger.debug('Processing call to Provider Upload Bulk Supporting Document API endpoint')
        with open(filename, 'rb') as fp:
            response        =   self.perform_api_call(
                                    method, apipath,
                                    self.username, self.apitoken,
                                    content_type=content_type, files={ 'upload': fp }
                                )
        
        return response


    def submit_bulk_initial_response(self, challenge_ids, **kwargs):
        """
        """
        assert isinstance(challenge_ids, list) and len(challenge_ids) <= 1000
        assert self.json['response_type'] in [ 'Accept', 'Reject' ]

        if self.json['response_type'] == 'Accept':
            assert self.json['response_file_id'] is not None

        method          =   'POST'
        apipath         =   '/api/vendor/submission/crowdsource/bulk/fixed/response'
        content_type    =   'application/json'

        json_body       =   {   'ids': challenge_ids,
                                **self.json }

        self.logger.debug('Processing call to Provider Submit Bulk Initial Response API endpoint')
        response        =   self.perform_api_call(
                                method, apipath,
                                self.username, self.apitoken,
                                content_type=content_type,
                                json=json_body
                            )
        
        return response


    def submit_bulk_final_response(self, challenge_ids, **kwargs):
        """
        """
        assert isinstance(challenge_ids, list) and len(challenge_ids) <= 1000
        assert self.json['final_response_type'] in [ 'Accept', 'Reject' ]

        if self.json['final_response_type'] == 'Reject':
            assert self.args['resolution_outcome_code'] in [ 1, 2, 3, 4, 5, 6, 7, 8, 99 ]
            assert self.args['challenger_concurrence'] in [ 'Yes', 'No', 'Unable to reach' ]

        method          =   'POST'
        apipath         =   '/api/vendor/submission/crowdsource/bulk/response/updateFixedChallengeFinalResponse'
        content_type    =   'application/json'

        json_body       =   {   'ids':  challenge_ids,
                                **self.json     }

        self.logger.debug('Processing call to Provider Submit Bulk Final Response API endpoint')
        response        =   self.perform_api_call(
                                method, apipath,
                                self.username, self.apitoken,
                                content_type=content_type, json=json_body
                            )
        
        return response


    def certify_bulk_response(self, challenge_ids, **kwargs):
        """
        """
        assert isinstance(challenge_ids, list) and len(challenge_ids) <= 1000
        assert self.json['certify_update_type'] in [ 'Remove', 'Update' ]

        if self.json['certify_update_type'] == 'Update':
            assert self.json['certify_update_technology'] in [ 10, 40, 50, 60, 61, 70, 71, 72, 0 ]
            assert isinstance(self.json['certify_update_download'], int)
            assert isinstance(self.json['certify_update_upload'], int)

        method          =   'POST'
        apipath         =   '/api/vendor/submission/crowdsource/bulk/response/updateFixedChallengeUpdateCertify'
        content_type    =   'application/json'

        json_body       =   {   'ids':  challenge_ids,
                                **self.json }

        self.logger.debug('Processing call to Provider Certify Bulk Response API endpoint')
        response        =   self.perform_api_call(
                                method, apipath,
                                self.username, self.apitoken,
                                content_type=content_type, json=json_body
                            )
        
        return response


    def revert_bulk_initial_response(self, challenge_ids, **kwargs):
        """
        """
        assert isinstance(challenge_ids, list) and len(challenge_ids) <= 1000

        method          =   'POST'
        apipath         =   '/api/vendor/submission/crowdsource/bulk/response/updateFixedChallengeRevertResponse'
        content_type    =   'application/json'

        json_body       =   {   'ids':  challenge_ids   }

        self.logger.debug('Processing call to Provider Revert Bulk Initial Response API endpoint')
        response        =   self.perform_api_call(
                                method, apipath,
                                self.username, self.apitoken,
                                content_type=content_type, json=json_body
                            )
        
        return response


    def revert_bulk_final_response(self, challenge_ids, **kwargs):
        """
        """
        assert isinstance(challenge_ids, list) and len(challenge_ids) <= 1000

        method          =   'POST'
        apipath         =   '/api/vendor/submission/crowdsource/bulk/response/updateFixedChallengeRevertFinalResponse'
        content_type    =   'application/json'

        json_body       =   {   'ids':  challenge_ids   }

        self.logger.debug('Processing call to Provider Revert Bulk Final Response API endpoint')
        response        =   self.perform_api_call(
                                method, apipath,
                                self.username, self.apitoken,
                                content_type=content_type, json=json_body
                            )
        
        return response
    
    