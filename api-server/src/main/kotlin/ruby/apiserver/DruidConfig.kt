package ruby.apiserver

import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.http.MediaType
import org.springframework.web.client.RestClient

@ConfigurationProperties(prefix = "druid")
data class DruidProperties(
    val baseUrl: String = "http://localhost:8888"
)

@Configuration
class DruidConfig(private val druidProperties: DruidProperties) {

    @Bean
    fun druidRestClient(): RestClient {
        return RestClient.builder()
            .baseUrl(druidProperties.baseUrl)
            .defaultHeaders { headers -> headers.contentType = MediaType.APPLICATION_JSON}
            .build()
    }
}
