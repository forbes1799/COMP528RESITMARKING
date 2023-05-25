<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CA2 Leaderboard</title>
  <meta name="description" content="CA2 Leaderboard">
  <meta name="author" content="Navjot Kukreja">
    <style type="text/css">
        .styled-table thead tr {
            background-color: #009879;
            color: #ffffff;
            text-align: left;
        }

        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
        }

        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
        }

        .styled-table tbody tr {
            border-bottom: thin solid #dddddd;
        }

        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }

        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #009879;
        }
    </style>
</head>
<body>
    <h1>League table for CA2</h1>
    <p></p>
    <table class="styled-table">
        <thead>
            <tr>
                <th>Serial No.</th>
                % for column in columns:
                <th>${column}</th>
                % endfor
            </tr>
        </thead>
        <tbody>
            % for i, row in enumerate(rows):
            <tr>
                <th>${i+1}.</th>
                % for column in columns:
                <th>${row[column]}</th>
                % endfor
            </tr>
            % endfor
        </tbody>
    </table>

    <h6>Last updated at ${time}, next update expected at ${next_time}.</h6>
</body>
</html>