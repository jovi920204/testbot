from main import GoogleAPIClient
from pprint import pprint
class GoogleSheets(GoogleAPIClient):
    def __init__(self) -> None:
        # 呼叫 GoogleAPIClient.__init__()，並提供 serviceName, version, scope
        super().__init__(
            'sheets',
            'v4',
            ['https://www.googleapis.com/auth/spreadsheets'],
        )
    def getWorksheet(self, spreadsheetId: str, range: str):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=spreadsheetId,
            range=range,
        )
        response = request.execute()
        return response
if __name__ == '__main__':
    myWorksheet = GoogleSheets()
    pprint(myWorksheet.getWorksheet(
        spreadsheetId='1-Z71G5IrXe3oUCXqHVSao_lqksUy7u6Hi07YdoTKHZA',
        range='2F'
    ))