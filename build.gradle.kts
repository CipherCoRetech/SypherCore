// Top-level build.gradle.kts file for the SypherCore project
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.8.21" // Update to latest version as per your project
    id("application")
    id("com.github.johnrengelman.shadow") version "7.1.0" // For packaging
}

group = "com.syphercore"
version = "1.0.0-SNAPSHOT"

repositories {
    // Central repositories to fetch dependencies
    mavenCentral()
    jcenter() // Optional
    maven("https://jitpack.io") // Custom dependencies like zk-SNARKs support libraries
}

dependencies {
    // Kotlin Standard Library
    implementation(kotlin("stdlib"))
    
    // Hedera SDK
    implementation("com.hedera.hashgraph:sdk:2.4.0") // Replace with the latest compatible version

    // BouncyCastle for cryptographic features
    implementation("org.bouncycastle:bcprov-jdk15on:1.70")

    // zk-SNARKs and Zero Knowledge Libraries (ZoKrates, Circom compatibility)
    implementation("io.zokrates:zokrates:0.7.7") // ZoKrates integration if using Java bindings
    implementation("com.github.iden3.circomlib:circomlib:0.2.0") // Circom libraries

    // JSON for config management
    implementation("com.fasterxml.jackson.core:jackson-databind:2.13.3")

    // Ring Signature Library
    implementation("org.bouncycastle:bcpg-jdk15on:1.70") // If implementing a ring signature

    // Logging
    implementation("org.slf4j:slf4j-api:1.7.32")
    implementation("ch.qos.logback:logback-classic:1.2.6")
    testImplementation("junit:junit:4.13.2")
}

application {
    // Main class reference for execution
    mainClass.set("com.syphercore.MainKt")
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "1.8" // Define JVM compatibility
}

tasks {
    // Custom build task to include zk-SNARK proof verification and signature generation logic
    register<Exec>("runZkSnarkSetup") {
        group = "build"
        description = "Set up zk-SNARK proving and verifying keys for Circom"
        commandLine = listOf(
            "bash", "-c",
            "cd src/main/circuits && zokrates compile -i proof.circom"
        )
    }

    register<Exec>("generateProof") {
        group = "build"
        description = "Generate proof using the compiled circuit"
        commandLine = listOf(
            "bash", "-c",
            "cd src/main/circuits && zokrates compute-witness -a input.json && zokrates generate-proof"
        )
    }

    // Clean Task
    register<Delete>("cleanGenerated") {
        group = "build"
        description = "Cleans up zk-SNARK generated proof files"
        delete("src/main/circuits/out")
    }

    named("clean") {
        dependsOn("cleanGenerated")
    }

    // Build Task
    named("build") {
        dependsOn("runZkSnarkSetup")
    }
}
