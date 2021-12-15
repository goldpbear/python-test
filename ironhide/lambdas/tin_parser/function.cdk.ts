import * as path from 'path'
import * as lambda from '@aws-cdk/aws-lambda'
import * as iam from '@aws-cdk/aws-iam'
import * as ssm from '@aws-cdk/aws-ssm'
import * as events from '@aws-cdk/aws-events'
import * as cdk from '@aws-cdk/core'
import { LambdaWithPermissions, LambdaWithPermissionsProps } from '@constructs/basic'
import { iam_perms, EnvironmentTypes } from '@constructs/utils'

const functionName = 'TINParser'

export interface LambdaFunctionProps {
  eventBus: events.EventBus,
  environment: EnvironmentTypes,
}

export const lambdaFunction = (
  scope: cdk.Stack,
  props: LambdaFunctionProps
): void => {
  // Standard params
  const serviceApiUrl = ssm.StringParameter.valueForStringParameter(
    scope, '/veda/SERVICE_API_URL'
  )
  const serviceApiId = ssm.StringParameter.valueForStringParameter(
    scope, '/veda/SERVICE_API_ID'
  )
  const artifactBucket = ssm.StringParameter.valueForStringParameter(
    scope, '/veda/ARTIFACT_BUCKET'
  )

  const funcProps: LambdaWithPermissionsProps = {
    eventBus: props.eventBus,
    functionProps: {
      functionName: functionName,
      code: lambda.Code.fromAsset(path.join(__dirname)),
      handler: 'index.handler',
      runtime: lambda.Runtime.PYTHON_3_7,
      timeout: cdk.Duration.minutes(5),
      memorySize: 2048,
      reservedConcurrentExecutions: 20,
      environment: {
        ENVIRONMENT: 'production',
        SERVICE_API_URL: serviceApiUrl,
        SERVICE_API_ID: serviceApiId
      },
    } as lambda.FunctionProps,
    functionPolicies: [
      new iam.PolicyStatement({
        actions: [...iam_perms.S3_GET, ...iam_perms.S3_PUT],
        resources: [
          `arn:aws:s3:::${artifactBucket}`,
          `arn:aws:s3:::${artifactBucket}/*`
        ]
      }),
    ],
    environment: props.environment
  }

  new LambdaWithPermissions(scope, functionName, funcProps)
}
