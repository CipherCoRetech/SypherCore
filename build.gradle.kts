import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.8.0"
    application
}

group = "com.syphercore"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))
    // Add any additional dependencies you need here, e.g., Hedera SDK
    implementation("com.hedera.hashgraph:sdk:2.0.0") // Update the version accordingly

    testImplementation(kotlin("test"))
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "1.8"
}

application {
    // Replace this with the actual path of your main entry class
    mainClass.set("com.syphercore.myapp.MainKt")
}

tasks.test {
    useJUnitPlatform()
}
