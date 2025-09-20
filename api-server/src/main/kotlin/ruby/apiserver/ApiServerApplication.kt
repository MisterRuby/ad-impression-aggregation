package ruby.apiserver

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.EnableConfigurationProperties
import org.springframework.boot.runApplication

@SpringBootApplication
@EnableConfigurationProperties(DruidProperties::class)
class ApiServerApplication

fun main(args: Array<String>) {
    runApplication<ApiServerApplication>(*args)
}
