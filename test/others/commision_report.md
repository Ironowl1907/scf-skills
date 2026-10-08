/prep
As a sales manager, I want to export the monthly commission report to CSV
so I can send it to payroll without retyping numbers.

Notes from the planning meeting:
- Should include all reps, including the ones who left mid-month (Laura wasn't sure about this)
- "Monthly" means calendar month, I think, but finance closes on the 25th
- Amounts should match what's on the dashboard
- Probably works like the invoices export we already have
- I was thinking we just run a background job and drop the file in S3, that's the easiest way
- Needs to be done before the Q4 close
