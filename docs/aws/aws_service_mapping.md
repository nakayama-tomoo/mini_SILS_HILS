# AWS Service Mapping

## Purpose

This document maps the current Mini SILS/HILS PoC components to potential AWS services.

The objective is to understand why each AWS service may be required.

The objective is not service memorization.

## Current Local Architecture

MacBook
↓
Python SILS
↓
Result Files
↓
Evidence Files
↓
GitHub Repository

## AWS Mapping

| Current Component             | Purpose                    | AWS Service                          |
| ----------------------------- | -------------------------- | ------------------------------------ |
| MacBook execution environment | Execute SILS               | Amazon EC2 (Elastic Compute Cloud)   |
| Evidence files                | Preserve execution results | Amazon S3 (Simple Storage Service)   |
| Local execution logs          | Monitor execution history  | Amazon CloudWatch                    |
| Local user account            | Access control             | IAM (Identity and Access Management) |
| GitHub repository             | Source code management     | GitHub (unchanged)                   |

## AWS Adoption Order

### Step 1

Amazon EC2

Goal:

Execute mini SILS successfully.

### Step 2

Amazon S3

Goal:

Store generated evidence.

### Step 3

Amazon CloudWatch

Goal:

Review execution logs.

### Step 4

GitHub Actions integration

Goal:

Trigger AWS execution from CI.

## Key Learning Principle

Learning order:

Current State
↓
Desired State
↓
Gap
↓
General Solution
↓
AWS Service

AWS services should be learned as solutions to problems.

They should not be memorized independently.

