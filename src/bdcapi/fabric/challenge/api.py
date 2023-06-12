# -*- coding: utf-8 -*-

from bdcapi.common.api import BaseAPITask


class EntityChallengeAPITask(BaseAPITask):

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


    def fab_withdraw_challenge(self, challenge_ids, **kwargs):
        """
        """
        assert isinstance(challenge_ids, list) and len(challenge_ids) <= 1000

        method          =   'POST'
        apipath         =   '/api/vendor/submission/crowdsource/fabric/bulk/withdraw'
        content_type    =   'application/json'

        json_body       =   {   'ids': challenge_ids,
                                **self.json }

        self.logger.debug('Processing call to Challenger Withdraw Challenges API endpoint')
        response        =   self._bdc_api_call(
                                method, apipath,
                                self.username, self.apitoken,
                                content_type=content_type,
                                json=json_body
                            )
        
        return response


#
#
#