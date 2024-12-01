plugins {
    kotlin("jvm") version "1.8.0"
    application
}

repositories {
    mavenCentral()
}
dependencies {
    implementation(kotlin("stdlib"))
    implementation("com.google.guava:guava:31.0.1-jre")
    implementation("com.hedera.hashgraph:sdk:2.15.1") // Update version as needed
}

dependencies {
    implementation(kotlin("stdlib"))
    implementation("com.google.guava:guava:31.0.1-jre")
    // Add additional dependencies here
}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
    kotlinOptions.jvmTarget = "1.8"
}
