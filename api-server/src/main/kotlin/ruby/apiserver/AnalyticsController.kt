package ruby.apiserver

import org.springframework.core.ParameterizedTypeReference
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.client.RestClient

@RestController
@RequestMapping("/api/analytics")
class AnalyticsController(
    private val druidRestClient: RestClient
){

    @GetMapping("/channels")
    fun getChannelImpressions(): ApiResponse<List<Map<String, Any>>> {
        val query = DruidQuery(
            queryType = "groupBy",
            dataSource = "ad-impressions",
            intervals = listOf("2024-01-01/2025-12-31"),
            granularity = "all",
            dimensions = listOf("channel_id"),
            aggregations = listOf(mapOf("type" to "count", "name" to "count"))
        )

        return druidRestClient.post()
            .uri("/druid/v2")
            .body(query)
            .retrieve()
            .body(object : ParameterizedTypeReference<List<Map<String, Any>>>() {})
            ?.let {
                ApiResponse(success = true, data = it, message = "${it.size} 개 채널의 노출량을 조회했습니다.")
            } ?: ApiResponse(success = false, message = "노출량 조회를 실패했습니다.")
    }

    @GetMapping("/regions")
    fun getRegionImpressions(): ApiResponse<List<Map<String, Any>>> {
        val query = DruidQuery(
            queryType = "groupBy",
            dataSource = "ad-impressions",
            intervals = listOf("2024-01-01/2025-12-31"),
            granularity = "all",
            dimensions = listOf("region_code"),
            aggregations = listOf(mapOf("type" to "count", "name" to "count"))
        )

        return druidRestClient.post()
            .uri("/druid/v2")
            .body(query)
            .retrieve()
            .body(object : ParameterizedTypeReference<List<Map<String, Any>>>() {})
            ?.let {
                ApiResponse(success = true, data = it, message = "${it.size} 개 지역의 노출량을 조회했습니다.")
            } ?: ApiResponse(success = false, message = "노출량 조회를 실패했습니다.")
    }
}

data class DruidQuery(
    val queryType: String,
    val dataSource: String,
    val intervals: List<String>,
    val granularity: String,
    val dimensions: List<String>,
    val aggregations: List<Map<String, Any>>
)

data class ApiResponse<T>(
    val success: Boolean,
    val data: T? = null,
    val message: String? = null
)
