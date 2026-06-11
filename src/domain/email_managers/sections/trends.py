from domain.models import Trend


def trends_card(trends: list[Trend]) -> str:
    trends = [trend for trend in trends if trend.ivs >= 0.0]
    rows = []
    if trends:
        for trend in trends:
            keywords = (
                ", ".join(trend.keywords)
                if trend.keywords
                else "No hay keywords para este trend"
            )
            row = f"""
                <tr>
                    <td>
                        <p style="font-weight:600; font-size: 14pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Trend: {trend.trend}
                        </p>
                        <p style="font-size: 8pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Keywords: {keywords}
                        </p>
                        <p style="font-size: 12pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Categoría: {trend.category}
                        </p>
                        <p style="font-size: 12pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Resumen:
                        </p>
                        <p style="text-indent: 2em; font-size: 10pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            {trend.news_summary if trend.news_summary is not None else "No se han encontrado noticias en los medios que seguimos"}
                        </p>
                        <p style="font-size: 12pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Métricas:
                        </p>
                        <p style="text-indent: 2em; font-size: 10pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            IVS: {round(trend.ivs, 2)}
                        </p>
                        <p style="text-indent: 2em; font-size: 10pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Demand Factor: {round(trend.demand_factor, 2)}
                        </p>
                        <p style="text-indent: 2em; font-size: 10pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Coverage Factor: {round(trend.coverage_factor, 2)}
                        </p>
                        <p style="text-indent: 2em; font-size: 10pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Delay Factor: {round(trend.delay_factor, 2)}
                        </p>
                        <p style="text-indent: 2em; font-size: 10pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Plurality Factor: {round(trend.plurality_factor, 2)}
                        </p>
                        <p style="text-indent: 2em; font-size: 10pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                            Volume: {trend.search_volume}
                        </p>
                    </td>
                </tr>
                <tr>
                    <td height="16" style="line-height: 0; font-size: 0;">&nbsp;</td> <!-- Spacer row -->
                </tr>
                """
            rows.append(row)
    else:
        row = """
            <tr>
                <td>
                    <p style="font-size: 12pt; color: #020617; margin: 0 0 8px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                        Ningún Trend de hoy supera el umbral de riesgo de 0.4 en IVS!
                    </p>
                </td>
            </tr>
            """
        rows.append(row)
    rows = "\n".join(rows)
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="border-left: solid 1px #475569; padding: 4px 32px;">
                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                        <td>
                            <p style="color: #10299f; font-weight:600; font-size: 16pt; margin: 0 0 20px; font-family: Helvetica Neue, Helvetica, sans-serif;">
                                Trends de búsqueda de hoy con riesgo por vacío de información
                            </p>
                        </td>
                    </tr>
                    {rows}
                </table>
            </td>
        </tr>
        <tr>
            <td height="24" style="line-height: 0; font-size: 0;">&nbsp;</td> <!-- Spacer row -->
        </tr>
    </table>
    """
