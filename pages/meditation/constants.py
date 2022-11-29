SQL = """"SELECT
	SEC_TO_TIME(SUM(TIMESTAMPDIFF(SECOND, `start`,`end`)))
FROM meditation m """
