import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.8.0"
    application
    id("com.github.ben-manes.versions") version "0.42.0" // Plugin for managing versions
    id("org.owasp.dependencycheck") version "8.1.0" // OWASP dependency-check plugin
}

group = "com.syphercore"
version = "1.0.0"

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(17))
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))
    
    // Update to the latest version of Hedera SDK
    implementation("com.hedera.hashgraph:sdk:2.45.0")
    
    // Cryptographic library for ring signatures
    implementation("org.bouncycastle:bcprov-jdk15on:1.70")
    
    // Example placeholder for zk-SNARK library
    // Ensure compatibility with JVM and Kotlin (could require using JNI bindings)

    testImplementation(kotlin("test"))
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "17"
}

application {
    // Replace this with the actual path of your main entry class
    mainClass.set("com.syphercore.myapp.MainKt")
}

tasks.test {
    useJUnitPlatform()
}
